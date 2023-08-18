#!/usr/bin/env python

__authors__ = ["Peter W. Njenga"]
__copyright__ = "Copyright © 2023 The Reframery, Co."

# Standard Libraries

# External Libraries
from pydantic import BaseModel, Field

# Internal Libraries
from typing import Optional, Dict, List, Any

from pydantic.types import UUID, Json
from uuid6 import uuid7
from validators import uuid

from reframe.server.lib.db_connection import Database

class Namespace(BaseModel):
    id_: UUID = Field(alias="_id", default_factory=uuid7)
    slug: str
    name: str
    trace_db: Optional[Database] = None
    trace_db_params: Optional[Dict[str, str]] = {}
    data_db: Optional[Database] = None
    data_db_params: Optional[Dict[str, str]] = {}

class Job(BaseModel):
    id_: UUID = Field(alias="_id", default_factory=uuid7)
    prompt: Any | None = None
    prompt_format_version: str
    initiator_id: UUID
    initiator_type: str = None
    engine_vs: str = "v0.0.1"
    read_cache: bool
    write_cache: bool
    table_name: str
    input_params: Any | None = None
    output_params: Any | None = None
