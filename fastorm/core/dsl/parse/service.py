import re
from importlib import import_module

from sqlglot import exp, parse_one
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import Scope, build_scope

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
    import_module(".dbschema", package="dbschema")  # TODO change for robust
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
    parent_node = next(root.walk())
    match parent_node:
        case exp.Select():
            if not parent_node.parent_select:
                for column_exp in parent_node.selects:
                    column: exp.Column = column_exp.this
                    table_name = _get_table_name(
                        column=column,
                        scope=root,
                    )
                    result.append(
                        dto.ColumnDTO(
                            name=column.name,
                            table=table_name,
                            python_type=Base.schema(pythonic=True)
                            .get(table_name, {})
                            .get(column.name, ""),  # type: ignore
                        )
                    )
    parameters = _parse_parameters(query=query)
    return dto.ParseResultDTO(
        sql_query=result_query,
        result_columns=result,
        parameters=parameters,
    )


def _get_table_name(column: exp.Column, scope: Scope) -> str:
    column_source = scope.sources.get(column.table)
    match column_source:  # noqa
        case Scope():
            return _get_table_name(column=column, scope=column_source)
        case exp.Table():
            return column_source.name
        case _:
            # TODO pretty exc
            raise Exception


def _parse_parameters(query: str) -> list[dto.ParameterDTO]:
    """Parse query and extract anme and types of parameters.

    Args:
        query (str): Raw sql query.

    Returns:
        list[dto.ParameterDTO]: Parsed parameters.
    """
    pattern = r"@(\w+):(\w+)"
    parameters = []

    matches = re.findall(pattern, query)

    for p_name, p_type in matches:
        parameters.append(
            dto.ParameterDTO(
                name=p_name,
                parameter_type=p_type,
            )
        )
    return parameters
