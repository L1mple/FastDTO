import os
import shutil
from pathlib import Path

import fastorm.common.errors as errors
from fastorm.common.errors import FastORMError


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
