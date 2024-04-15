from importlib import import_module

from sqlglot import exp, parse_one
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import build_scope, find_all_in_scope

from fastorm.common import dto
from fastorm.core.dsl.schema.base import Base


def parse_query(query: str) -> dto.ParseResultDTO:
    """Parse query and returns declarative DTO.

    Parse query to:
    - What columns are fetched
    - From which tables

    Args:
        query (str): Raw SQL query

    Returns:
        dto.ParseResultDTO: DTO of ParsedQuery.
    """
    result = []
    ast = parse_one(query)
    import_module(".dbschema", package="dbschema")
    qualify(
        expression=ast,
        schema=Base.schema(),
        expand_alias_refs=False,
        validate_qualify_columns=False,
        quote_identifiers=False,
        identify=False,
    )
    result_query = ast.sql()
    qualify(
        expression=ast,
        schema=Base.schema(),
    )
    root = build_scope(ast)
    if root is None:
        # TODO raise exception
        raise Exception
    for column in find_all_in_scope(root.expression, exp.Column):
        column: exp.Column
        result.append(
            dto.ColumnDTO(
                name=column.name,
                table=root.sources[column.table].name,
                python_type=Base.schema(pythonic=True)
                .get(root.sources[column.table].name, {})
                .get(column.name, ""),
            )
        )
    return dto.ParseResultDTO(
        sql_query=result_query,
        result_columns=result,
    )
