"""File contains all possible errors that FastORM can raise."""


class FastORMError(Exception):
    """Base class for other Errors."""

    ...


class DirectoryAlreadyExistsError(FastORMError):
    """Error for `init` command."""

    ...


class DirectoryCreateError(FastORMError):
    """Error for `init` command."""

    ...
