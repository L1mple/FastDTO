from sqlglot.expressions import DataType


class Column:
    """Base class for column declaration in DSL file."""

    def __init__(
        self,
        column_type: str | DataType.Type | DataType,
        python_type: str,
    ):  # TODO extend parameters and change from str to Enum?
        self.column_type = column_type
        self.python_type = python_type

    @property
    def sql_type(self):
        """Returns type for sqlglot lib.

        Returns:
            _type_: _description_  # TODO typing
        """
        return self.column_type

    @property
    def dto_type(self):
        """# TODO typing."""
        return self.python_type
