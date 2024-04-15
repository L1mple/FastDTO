import os
import shutil
from io import StringIO
from pathlib import Path

import fastorm.common.errors as errors
from fastorm.common import dto
from fastorm.common.errors import FastORMError
from fastorm.common.utils import to_camel_case, to_snake_case
from fastorm.core.dsl.parse.service import parse_query

INDENT = "    "


def init_project_structure(directory: str) -> None | FastORMError:
    """Create directory and files for DB schema.

    Returns:
        None | FastORMError: None if all good, Error if smth wrong
    """
    import fastorm

    package_dir = Path(os.path.abspath(os.path.dirname(fastorm.__file__)))
    templates_path = package_dir.joinpath("templates")
    if os.access(directory, os.F_OK) and os.listdir(directory):
        raise errors.DirectoryAlreadyExistsError(
            f"Directory {directory} already exists and not empty"
        )

    try:
        shutil.copytree(templates_path.joinpath("init"), directory)
    except Exception as exc:
        raise errors.DirectoryCreateError(
            "Something went wrong while creating directory"
        ) from exc


def generate_orm_code(filename: str, scripts_dir: str) -> None | FastORMError:
    """Generates file that contains scripts with DTO mapping.

    Args:
        filename (str): Filename
        scripts_dir (str): Directory that has .sql files

    Returns:
        None | FastORMError: None if all good, Error if smth wrong
    """
    buf = StringIO()
    _generate_imports(buffer=buf)
    for file_or_dir in Path(scripts_dir).iterdir():
        if not file_or_dir.exists():
            continue
        if file_or_dir.suffix.lower() == ".sql":
            with file_or_dir.open() as f:
                query = f.read()
            parsed_query = parse_query(query=query)
            _generate_func_for_query(
                name=file_or_dir.stem,
                buffer=buf,
                parsed_query=parsed_query,
            )
    with Path(scripts_dir).joinpath(filename + ".py").open("w") as f:
        f.write(buf.getvalue())


def _generate_imports(buffer: StringIO) -> StringIO:
    """Generates imports for codegen functions.

    Args:
        buffer (StringIO): Buffer to save current progress of generated file.

    Returns:
        StringIO: Writed buffer.
    """
    print("from fastorm.connection import IAsyncExecutor", file=buffer)
    print(
        "from fastorm.core.codegen.model import FastORMModel",
        end="\n\n\n",
        file=buffer,
    )
    return buffer


def _generate_func_for_query(
    name: str,
    buffer: StringIO,
    parsed_query: dto.ParseResultDTO,
) -> StringIO:
    """Generates function for specific query.

    Args:
        name (str): Name of file with query without file extenstion (without .sql).
        parsed_query (dto.ParseResultDTO): Parsed SQL query with metadata.
        buffer (StringIO): Buffer to save current progress of generated file.

    Returns:
        StringIO: Saved buffer.
    """
    print(f"class {to_camel_case(name)}Result(FastORMModel):", file=buffer)
    for column in parsed_query.result_columns:
        print(f"{INDENT}{column.name}: {column.python_type}", file=buffer)
    print(end="\n\n", file=buffer)
    print(f"async def {to_snake_case(name)}(", file=buffer)
    print(f"{INDENT}executor: IAsyncExecutor,", file=buffer)
    print(f") -> list[{to_camel_case(name)}Result]:", file=buffer)
    print(f"{INDENT}result = await executor.execute(", file=buffer)
    print(f'{INDENT * 2}"""', file=buffer)
    print(f"{INDENT * 2}{parsed_query.sql_query}", file=buffer)
    print(f'{INDENT * 2}"""', file=buffer)
    print(f"{INDENT})", file=buffer)
    print(
        f"{INDENT}return [{to_camel_case(name)}Result.from_list(row) for row in result]",  # noqa:E501
        end="\n\n\n",
        file=buffer,
    )
    return buffer
