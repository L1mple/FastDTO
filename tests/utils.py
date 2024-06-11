import functools
from typing import Callable
from unittest.mock import patch

from fastdto.common.mappings import TO_PYTHON


def patch_schema_for_test(user_schema: dict):
    """Util decorator for easier testing.

    Args:
        user_schema (dict): User's defined schema for test.
    """

    def decorator(test_func: Callable):
        @functools.wraps(test_func)
        def wrapper(*args, **kwargs):
            def test_schema_mock(pythonic: bool | None = None) -> dict:
                """Special side effect schema for tests.

                Args:
                    pythonic (bool): Is schema needed in pythonic types.

                Returns:
                    dict: Schema object.
                """
                if pythonic:
                    return convert_schema_to_pythonic(user_schema)
                return user_schema

            with patch("fastdto.core.dsl.schema.base.Base.schema") as mock_func:
                mock_func.side_effect = test_schema_mock
                return test_func(*args, **kwargs)

        return wrapper

    return decorator


def convert_schema_to_pythonic(d: dict | str):
    """Convert nested dict schema to pythonic format.

    Args:
        d (dict | str): Nested dict with schema

    Returns:
        None: None
    """
    if isinstance(d, dict):
        return {key: convert_schema_to_pythonic(value) for key, value in d.items()}
    return TO_PYTHON[d]
