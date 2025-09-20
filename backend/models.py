from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class DataSourceType(str, Enum):
    FLAT_FILE = "flat_file"
    DB2_TABLE = "db2_table"
    GREEN_SCREEN = "green_screen"
    RPG_PROGRAM = "rpg_program"

class FieldMapping(BaseModel):
    legacy_field: str
    modern_field: str
    data_type: str
    description: str
    transformation_rule: Optional[str] = None

class TableSchema(BaseModel):
    table_name: str
    fields: List[FieldMapping]
    primary_key: List[str]
    indexes: List[str] = []

class APISpec(BaseModel):
    endpoint: str
    method: str
    description: str
    parameters: List[Dict[str, Any]]
    response_schema: Dict[str, Any]

class Microservice(BaseModel):
    name: str
    description: str
    endpoints: List[APISpec]
    dependencies: List[str] = []
    dockerfile: Optional[str] = None

class LegacyData(BaseModel):
    id: str
    source_type: DataSourceType
    content: str
    metadata: Dict[str, Any]
    created_at: datetime
    processed: bool = False

class ModernizedData(BaseModel):
    id: str
    legacy_id: str
    modern_schema: TableSchema
    api_specs: List[APISpec]
    microservices: List[Microservice]
    transformation_log: List[str]
    created_at: datetime

class QueryRequest(BaseModel):
    table_name: str
    filters: Dict[str, Any] = {}
    limit: int = 100
    offset: int = 0

class QueryResponse(BaseModel):
    data: List[Dict[str, Any]]
    total_count: int
    query_time: float
