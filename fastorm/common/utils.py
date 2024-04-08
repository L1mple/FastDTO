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
