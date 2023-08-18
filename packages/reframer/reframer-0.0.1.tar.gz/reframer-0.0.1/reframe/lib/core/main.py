#!/usr/bin/env python

__authors__ = ["Peter W. Njenga"]
__copyright__ = "Copyright © 2023 The Reframery, Co."

# Standard Libraries
import asyncio
import os
import json
from pprint import pprint, pformat

# External Libraries
import psycopg
import redis
from os import environ as env
import tiktoken
import jinja2
from dotenv import load_dotenv
from loguru import logger
from psycopg import sql
import openai

# Internal Libraries
from reframe.lib.core import RedisStreamProcessor
from reframe.lib.models.chat import openai_chat
from reframe.lib.utils import fmt_payload

# Global Variables
CACHE_EXPIRATION_DURATION = 60 * 60 * 24 * 90 # 90 days
TASK_EXPIRATION_DURATION = 60 * 60 * 24 * 2 # 48 Hours

REDIS_STREAM_HOST=os.environ.get('REDIS_STREAM_HOST', "localhost")
REDIS_CACHE_HOST=os.environ.get('REDIS_CACHE_HOST', "localhost")
REDIS_PASSWORD=os.environ.get('REDIS_PASSWORD')
red_stream = redis.StrictRedis(
    REDIS_STREAM_HOST, 6379, charset="utf-8",
    password=REDIS_PASSWORD, decode_responses=True)
red_cache = redis.StrictRedis(
    REDIS_STREAM_HOST, 6379, charset="utf-8",
    password=REDIS_PASSWORD, decode_responses=True)
openai.api_key = os.environ['OPENAI_API_KEY']
jinja_env = jinja2.Environment()
# ------------------------------

class SingleActionChatAgent(RedisStreamProcessor):
    def __init__(self, name, invoke_commands, chat_template, tool_list=[], tool_graph={}, *args, **kwargs):
        load_dotenv()
        self.name = name
        self.invoke_commands = invoke_commands
        self.tool_graph = tool_graph
        self.tool_list = tool_list

        for _template in chat_template:
            _template["content"] = jinja_env.from_string(_template["content"])
        self.chat_template = chat_template

        super().__init__(instream_key=f"agent->{self.name}")

        self.new_event_loop = asyncio.new_event_loop()
        self.new_event_loop.run_until_complete(self.connect_to_db())
        logger.info(f"Initialized NNextAgent [name={name} invoke_commands={invoke_commands}]")

    def __del__(self):
        logger.info(f"Deconstructed NNextAgent [name={self.name}]")
        self.new_event_loop.stop()
        asyncio.run(self.disconnect_db())

    async def connect_to_db(self):
        PLAT_DB_HOST = env.get('PLAT_DB_HOST', 'localhost')
        PLAT_DB_USER = env.get('PLAT_DB_USER', 'postgres')
        PLAT_DB_PASS = env.get('PLAT_DB_PASS')
        PLAT_DB_NAME = env.get('PLAT_DB_NAME')

        self.data_db_conn = await psycopg.AsyncConnection.connect(
            host=PLAT_DB_HOST,
            user=PLAT_DB_USER,
            password=PLAT_DB_PASS,
            dbname=PLAT_DB_NAME,
            autocommit=True
        )

        self.data_db_cursor = self.data_db_conn.cursor()
        logger.debug(f"Connected to Platform DB {PLAT_DB_HOST}/{PLAT_DB_NAME}")

    async def disconnect_db(self):
        await self.data_db_conn.close()
        await self.data_db_cursor.close()

    def plan(self):
        raise NotImplementedError

    def get_last_processed_message_id(self):
        last_processed_message_id = red_stream.get(self.last_processed_stream_key)
        if last_processed_message_id is None:
            last_processed_message_id = "0-0"

        return last_processed_message_id

    def set_last_processed_message_id(self, message_id):
        last_processed_message_id = self.get_last_processed_message_id()

        old_ts, old_seq = last_processed_message_id.split("-")
        old_ts, old_seq = int(old_ts), int(old_seq)

        new_ts, new_seq = message_id.split("-")
        new_ts, new_seq = int(new_ts), int(new_seq)

        if new_ts > old_ts:
            last_processed_message_id = message_id
        elif new_ts == old_ts and new_seq > old_seq:
            last_processed_message_id = message_id
        else:
            print("!!!")
            exit(3)

        red_stream.set(self.last_processed_stream_key, last_processed_message_id)

        return last_processed_message_id

    # Send jobs to the agent tools.
    async def sow(self):
        last_processed_message_id = self.get_last_processed_message_id()
        # logger.debug(f"sow: stream_key: {self.instream_key}")
        l = red_stream.xread(count=5, streams={self.instream_key: last_processed_message_id}, block=500)

        # Iterate over the stream keys.
        for _k in l:
            stream_key, stream_messages = _k
            # Iterate over the message batch for that stream key.
            for _j in stream_messages:
                message_id, message_data = _j
                logger.debug(f"Received stream_key={stream_key}, message_id={message_id} message_data={pformat(message_data)}")
                tool_name = self.tool_list[0].get('name')

                tool_stream_key = f"nnext::instream::tool->{tool_name}"

                payload = json.loads(message_data['payload'])
                prompt_text = message_data['prompt_text']
                output_column = message_data['output_column']
                table_name = message_data['table_name']
                correlation_id = payload.get('_id')

                message = {
                    'payload': json.dumps(payload),
                    'correlation_id': correlation_id,
                    'agent': self.name,
                }

                logger.debug(f"Running tool->{tool_name} with payload->{(pformat(message))}")

                red_stream.xadd(tool_stream_key, message)

                task_key = f"nnext::task-pending::agent->{self.name}::correlation_id->{correlation_id}"
                red_cache.set(
                    task_key,
                    json.dumps({}, default=str),
                    ex=CACHE_EXPIRATION_DURATION
                )

                prompt_text_key = f"nnext::prompt-text::agent->{self.name}::correlation_id->{correlation_id}"
                red_cache.set(
                    prompt_text_key,
                    json.dumps({
                        "prompt_text": prompt_text,
                        "output_column": output_column,
                        "table_name": table_name
                    }, default=str),
                    ex=CACHE_EXPIRATION_DURATION
                )

                self.last_sow_key_processed = message_id

                self.set_last_processed_message_id(message_id)

    # Gather results from the result stream and place them into a set.
    async def reap(self):
        tool_name = self.tool_list[0].get('name')

        # Iterate over all the tools and get their results.
        tool_stream_key_map = {}
        for tool in self.tool_list:
            tool_stream_key = f"nnext::outstream::agent->{self.name}::tool->{tool.get('id')}"
            tool_stream_key_map[tool_stream_key] = 0
        l = red_stream.xread(count=3, streams=tool_stream_key_map, block=5)

        # Iterate over the stream keys.
        for stream_key, stream_messages in l:
            # Iterate over the message batch for that stream key.
            for message_id, message_data in stream_messages:
                red_stream.xdel(stream_key, message_id)

                correlation_id = message_data.get('correlation_id')
                payload = message_data.get('payload')

                logger.opt(ansi=True).info(f"Received result from tool->{tool.get('id')}. correlation_id->{correlation_id}, payload-><yellow>{fmt_payload(payload)}</yellow>")

                result_key = f"nnext::memory::agent->{self.name}::tool->{tool_name}[0]::elem->{correlation_id}"

                self.on_tool_result(tool_name, correlation_id, payload)

                red_stream.set(result_key, json.dumps(message_data, default=str))


    async def collate(self):
        key_prefix = f"nnext::task-pending::agent->{self.name}::correlation_id->*"
        for key in red_stream.scan_iter(key_prefix):
            correlation_id = key.split("::correlation_id->")[1]

            prompt_text_key = f"nnext::prompt-text::agent->{self.name}::correlation_id->{correlation_id}"
            llm_prompt = red_cache.get(prompt_text_key)
            if llm_prompt:
                llm_prompt = json.loads(llm_prompt)

            tools_result_set_complete = True
            db_result = None
            tool_result_map = {}
            # Check if all tools have completed.
            for tool in self.tool_list:
                tool_output_template = tool.get('output')
                tool_key = tool.get('name')
                tool_results = red_stream.get(
                    f"nnext::memory::agent->{self.name}::tool->{tool.get('id')}[0]::elem->{correlation_id}"
                )
                if tool_results is None:
                    tools_result_set_complete = False
                    break
                else:

                    tool_results = json.loads(tool_results)
                    payload = json.loads(tool_results.get('payload'))

                    # Check if the tool errored.
                    if payload.get('status').lower() == 'error':
                        logger.error(f"Tool->{tool_key} errored. correlation_id->{correlation_id}")
                        tools_result_set_complete = False
                        db_result = payload
                        red_stream.delete(key)
                        break

                tool_result_map[tool_output_template] = tool_results

            if tools_result_set_complete:
                prompt_text = llm_prompt.get('prompt_text')

                if "$GPT" in prompt_text:
                    prompt_text = prompt_text.split("$GPT")[1]

                tool_result_map['llm_prompt'] = prompt_text

                enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

                formated_template = []

                for _template in self.chat_template:
                    formated_content = _template["content"].render(tool_result_map)
                    tokenized = enc.encode(formated_content)

                    tokenized = tokenized[:3500]
                    tokenized_text = enc.decode(tokenized)

                    formated_template.append(
                        {"content": tokenized_text, "role": _template["role"]}
                    )

                # Call OpenAI API.
                # response = await openai_chat(formated_template)
                response = await openai_chat(formated_template, read_cache=False, write_cache=True)
                # TODO: Check that the result is indeed a success.
                db_result = {
                    "status": "SUCCESS",
                    "result": response
                }

                red_stream.delete(key)

                logger.debug(f"openai Result-->> {pformat(response)}")

                result_key = f"nnext::agent-results::agent->{self.name}::correlation_id->{correlation_id}"
                red_cache.set(result_key, response, ex=CACHE_EXPIRATION_DURATION)

            if db_result:
                # Store results in Redis and Postgres.
                output_column = llm_prompt.get('output_column')
                table_name = llm_prompt.get('table_name')

                # TODO
                # Probably call a on_db_write hook here.

                _sql_stmt = sql.SQL(
                    """
                    INSERT INTO {} (_id, {})
                    VALUES (%(_id)s, %(result)s)
                    ON CONFLICT (_id)
                    DO UPDATE SET
                    {}=EXCLUDED.{};
                    """
                ).format(
                    sql.Identifier(table_name),
                    sql.Identifier(output_column),
                    sql.Identifier(output_column),
                    sql.Identifier(output_column)
                )

                try:
                    logger.info(f"Inserting into table {table_name}. {output_column}⇨ {pformat(db_result)}")
                    await self.data_db_cursor.execute(_sql_stmt, {
                        "_id": correlation_id,
                        "result": json.dumps(db_result)
                    })
                except Exception as e:
                    logger.error(e)
                    logger.error(f"Error inserting into table {table_name}.")


    def on_tool_result(self, tool_name, correlation_id, payload):
        pass
        # Potentially raise a NotImplementedError here.

    def on_plan(self, plan):
        logger.debug(f"@on_plan Started plan->{plan}")

    async def wait_func(self, *args, **kwargs):
        await self.sow()
        await self.reap()
        await self.collate()

    def add_tool(self, tool):
        raise NotImplementedError

    def add_link(self, source, target):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        self.new_event_loop = asyncio.new_event_loop()
        try:
            while True:
                self.new_event_loop.run_until_complete(self.wait_func())
        except redis.exceptions.ConnectionError as redis_connection_error:
            logger.critical(
                f"Redis connection error: {redis_connection_error}. Is Redis running and variable 'REDIS_STREAM_HOST' set?")
        except Exception as e:
            logger.exception(e)
        finally:
            self.new_event_loop.close()