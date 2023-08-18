#!/usr/bin/env python

__authors__ = ["Peter W. Njenga"]
__copyright__ = "Copyright © 2023 The Reframery, Co."

# Standard Libraries
import json
from os import environ as os_env

# External Libraries
from fastapi import APIRouter, Request, Depends, HTTPException, status
from loguru import logger
from pprint import pformat, pprint
from psycopg import sql
from fastapi.encoders import jsonable_encoder

# Internal Libraries
from slugify import slugify
from uuid6 import uuid7

from reframe.server.lib.api_key import generate_api_key
from reframe.server.lib.auth.prisma import JWTBearer, decodeJWT
from reframe.server.lib.db_connection import Database
from reframe.server.lib.db_models.namespace import Namespace
from reframe.server.lib.prisma import prisma
import psycopg

# Global Variables
router = APIRouter()

class Serial(dict):
    def __getitem__(self, key):
        return f"${list(self.keys()).index(key) + 1}"

@router.post("/namespace/", name="Create Namespace", description="Create Workspace or Namespace")
async def create_namespace(request: Request, namespace: Namespace):
    """Agents endpoint"""
    try:
        namespace_id = uuid7()
        namespace.slug = slugify(namespace.slug, separator='_')
        trace_db_name = f"trace_{str(namespace_id).split('-')[3]}_{namespace.slug}"

        __namespace = {
            **namespace.dict(),
            "_id" : str(namespace_id),
            "trace_db_params": {
                "database": trace_db_name,
            }
        }

        namespace.data_db = Database(**namespace.data_db_params)

        await namespace.data_db.connect()
        request.app.state.data_db[namespace_id] = namespace.data_db

        await request.app.state.meta_db.execute(
            """ 
            INSERT INTO namespace (_id, slug, name, data_db_params, trace_db_params)
            VALUES (%(_id)s, %(slug)s, %(name)s, %(data_db_params)s, %(trace_db_params)s)
            RETURNING _id, slug, name
            """, __namespace)

        logger.info(f"Created new namespace: {pformat(__namespace)}")

        api_key = generate_api_key()
        await request.app.state.meta_db.execute(
            """
            INSERT INTO api_key (_id, key, namespace_id, name)
            VALUES (%(_id)s, %(key)s, %(namespace_id)s, %(name)s)
            RETURNING _id
            """, {
                "_id": uuid7(),
                "key": api_key,
                "namespace_id": namespace_id,
                'name': f"Default API Key for {namespace.name}"
            })

        logger.info("Created new API Key")

        await request.app.state.meta_db.execute(
            """
            CREATE DATABASE {db_name}
            """.format(db_name=trace_db_name)
        )
        logger.info(f"Created new database: {trace_db_name}")

        await request.app.state.meta_db.execute(
            """
            GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}
            """.format(db_name=trace_db_name, db_user="postgres")
        , {})

        # Connect to the new database and create the trace schema
        trace_db = Database(database=trace_db_name)
        await trace_db.connect()

        request.app.state.trace_db[trace_db_name] = trace_db

        await trace_db.execute(
            """
            CREATE SCHEMA IF NOT EXISTS trace
            """
        )

        await trace_db.execute(
            """
            CREATE EXTENSION IF NOT EXISTS moddatetime
            """
        )


        table_name = 'trace'
        await trace_db.execute(
            """
            CREATE TABLE trace.{table_name} (
                _id             uuid                            default gen_random_uuid()   not null    constraint {table_name}_pk primary key,
                _cr             timestamp   with time zone      default now()               not null,
                _up             timestamp   with time zone      default now()               not null,
                parent_id       uuid,
                entry           jsonb   not null,
                level           varchar(10) not null,
                job_id          uuid,
                correlation_id  uuid
            );
            
            CREATE INDEX {table_name}_id_idx ON trace.{table_name} (_id);
            """.format(table_name=table_name)
        )
        logger.info(f"Created new table: trace.{table_name}")

        table_name = 'job'
        await trace_db.execute(
            """
            CREATE TABLE trace.{table_name} (
                _id             uuid                            default gen_random_uuid()   not null    constraint {table_name}_pk primary key,
                _cr             timestamp   with time zone      default now()               not null,
                _up             timestamp   with time zone      default now()               not null,
                prompt                jsonb                                                         not null,
                prompt_format_version varchar(50)                                                   not null,
                initiator_id          uuid                                                          not null,
                initiator_type        varchar(25)                                                   not null,
                engine_vs             varchar(50)              default 'v0.0.01'::character varying not null,
                read_cache            boolean                  default true                         not null,
                write_cache           boolean                  default true                         not null,
                table_name              varchar(200)    not null,
                input_params            jsonb           not null,
                output_params           jsonb           not null
            );

            CREATE INDEX {table_name}_id_idx ON trace.{table_name} (_id);
            """.format(table_name=table_name)
        )
        logger.info(f"Created new table: trace.{table_name}")

        table_name = 'thread'
        await trace_db.execute(
            """
            CREATE TABLE trace.{table_name} (
                _id             uuid                            default gen_random_uuid()   not null    constraint {table_name}_pk primary key,
                _cr             timestamp   with time zone      default now()               not null,
                _up             timestamp   with time zone      default now()               not null,
                elem_id          uuid,
                group_id          uuid,
                dataframe_id          uuid,
                column_id          uuid
            );
            
            CREATE INDEX {table_name}_id_idx ON trace.{table_name} (_id);
            """.format(table_name=table_name)
        )
        logger.info(f"Created new table: trace.{table_name}")

        table_name = 'agent'
        await trace_db.execute(
            """
            CREATE TABLE {table_name} (
                _id             uuid                            default gen_random_uuid()   not null    constraint {table_name}_pk primary key,
                _cr             timestamp   with time zone      default now()               not null,
                _up             timestamp   with time zone      default now()               not null,
                name                varchar(50)                                             not null,
                slug                varchar(50)                                             not null unique,
                engine_vs             varchar(50)              default 'v0.0.01'::character varying not null,
                read_cache            boolean                  default true                         not null,
                write_cache           boolean                  default true                         not null
            );

            CREATE INDEX {table_name}_id_idx ON {table_name} (_id);
            """.format(table_name=table_name)
        )
        logger.info(f"Created new table: public.{table_name}")

        table_name = 'tool'
        await trace_db.execute(
            """
            CREATE TABLE {table_name} (
                _id             uuid                            default gen_random_uuid()   not null    constraint {table_name}_pk primary key,
                _cr             timestamp   with time zone      default now()               not null,
                _up             timestamp   with time zone      default now()               not null,
                name                varchar(50)                                             not null,
                slug                varchar(50)                                             not null unique,
                engine_vs             varchar(50)              default 'v0.0.01'::character varying not null,
                read_cache            boolean                  default true                         not null,
                write_cache           boolean                  default true                         not null
            );
            
            CREATE INDEX {table_name}_id_idx ON {table_name} (_id);
            """.format(table_name=table_name)
        )
        logger.info(f"Created new table: public.{table_name}")

        request.app.state.trace_db[trace_db_name] = trace_db

        logger.info(f"Done initializing namespace: {namespace}")

        __namespace.pop("db_name", None)
        __namespace.pop("trace_db", None)
        __namespace.pop("trace_db_params", None)
        __namespace.pop("data_db", None)
        __namespace.pop("data_db_params", None)
        __namespace.pop("id_", None)
        __namespace["api_key"] = api_key
        return {"success": True, "data": __namespace}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )




@router.get("/namespace/", name="List all namespaces", description="List all namespaces")
async def list_agents():
    """Agents endpoint"""
    decoded = decodeJWT(token)
    agents = prisma.agent.find_many(
        where={"userId": decoded["userId"]},
        include={
            "user": True,
        },
        order={"createdAt": "desc"},
    )

    if agents:
        return {"success": True, "data": agents}

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="No agents found",
    )


@router.get("/namespace/{namespace_id}/", name="Get namespace", description="Get a specific namespace")
async def read_namespace(namespace_id: str, token=Depends(JWTBearer())):
    """Agent detail endpoint"""
    agent = prisma.agent.find_unique(where={"id": namespace_id}, include={"prompt": True})

    if agent:
        return {"success": True, "data": agent}

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Agent with id: {namespace_id} not found",
    )


@router.delete(
    "/namespace/{namespace_id}/", name="Delete namespace", description="Delete a specific namespace"
)
async def delete_agent(namespace_id: str, token=Depends(JWTBearer())):
    """Delete agent endpoint"""
    try:
        prisma.agentmemory.delete_many(where={"namespace_id": namespace_id})
        prisma.agent.delete(where={"id": namespace_id})

        return {"success": True, "data": None}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
        )


@router.patch(
    "/agent/{namespace_id}/", name="Patch namespace", description="Patch a specific namespace"
)
async def patch_namespace(namespace_id: str, body: dict, token=Depends(JWTBearer())):
    """Patch agent endpoint"""
    try:
        prisma.agent.update(data=body, where={"id": namespace_id})

        return {"success": True, "data": None}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
        )