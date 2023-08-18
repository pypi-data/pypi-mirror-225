from pydantic import BaseModel
from typing import Dict, Any, List, Optional


class Pinecone_config(BaseModel):
    odb_url: str
    pinecone_key: str
    pinecone_env: str
    table_name: str
    column_names: list[str]


class Chroma_config(BaseModel):
    odb_url: str
    table_name: str
    column_names: list[str]


class Chroma_query(BaseModel):
    table_name: str
    text: str
    top_k: int


class ColumnInfo(BaseModel):
    name: str
    type: str

class TableInfo(BaseModel):
    table_name: str
    columns: List[ColumnInfo]

class SourceDBInfo(BaseModel):
    db_name: str
    db_type: str
    username: str
    password: str
    host: str
    port: str
    ssl_mode: str
    url: Optional[str]   # this is optional because of the '?' in your original TypeScript code
    db_id: int
    sync: bool

class SourceDB(BaseModel):
    tables: List[TableInfo]
    info: SourceDBInfo

class UserInfo(BaseModel):
    id: Optional[int]
    user_name: str
    user_email: str

class SelectedTable(BaseModel):
    table_name: str
    selected_columns: List[ColumnInfo]

class Message(BaseModel):
    user_info: UserInfo
    source_db: SourceDB
    selected_table: SelectedTable