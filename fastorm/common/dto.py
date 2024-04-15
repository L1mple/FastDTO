from pydantic import BaseModel


class ColumnDTO(BaseModel):
    """DTO for parsed column from SQL query."""

    name: str
    python_type: str
    table: str


class ParseResultDTO(BaseModel):
    """DTO for parsed query from SQL."""

    sql_query: str
    result_columns: list[ColumnDTO]
