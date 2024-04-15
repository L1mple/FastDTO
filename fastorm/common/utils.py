import os
from pathlib import Path
from re import sub


def to_snake_case(string: str) -> str:
    """Util function to convert string to snake case.

    Args:
        string (str): String to convert.

    Returns:
        str: Snakecased string.
    """
    string = (
        sub(
            r"(?<=[a-z])(?=[A-Z])|[^a-zA-Z]",
            " ",
            string,
        )
        .strip()
        .replace(" ", "_")
    )
    return "".join(string.lower())


def get_project_root() -> Path:
    """Returns path to project root.

    Returns:
        Path: Path agnostic to OS.
    """
    return Path(os.getcwd())


def to_camel_case(string: str) -> str:
    """Util function to convert string to camel case.

    Args:
        string (str): String to convert.

    Returns:
        str: Camelcased string.
    """
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return "".join([string[0].lower(), string[1:]]).capitalize()
