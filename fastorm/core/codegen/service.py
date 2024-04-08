import os
import shutil
from io import StringIO
from pathlib import Path

import fastorm.common.errors as errors
from fastorm.common.errors import FastORMError
from fastorm.common.utils import to_snake_case

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
            _generate_func_for_query(
                name=file_or_dir.stem,
                query=query,
                buffer=buf,
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
    print("from typing import Any", end="\n\n", file=buffer)
    print("from fastorm.connection import IAsyncExecutor", end="\n\n\n", file=buffer)
    return buffer


def _generate_func_for_query(
    name: str,
    query: str,
    buffer: StringIO,
) -> StringIO:
    """Generates function for specific query.

    Args:
        name (str): Name of file with query without file extenstion (without .sql).
        query (str): SQL query to parse and generate python func.
        buffer (StringIO): Buffer to save current progress of generated file.

    Returns:
        StringIO: Saved buffer.
    """
    query = query.replace("\n", f"\n{INDENT * 2}")
    print(f"async def {to_snake_case(name)}(", file=buffer)
    print(f"{INDENT}executor: IAsyncExecutor,", file=buffer)
    print(") -> Any:", file=buffer)
    print(f"{INDENT}return await executor.execute(", file=buffer)
    print(f'{INDENT * 2}"""', file=buffer)
    print(f"{INDENT * 2}{query}", file=buffer)
    print(f'{INDENT * 2}"""', file=buffer)
    print(f"{INDENT})", end="\n\n\n", file=buffer)
    return buffer
