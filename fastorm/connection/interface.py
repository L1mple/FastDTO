from typing import Protocol


class IAsyncExecutor(Protocol):
    """General interface for user code executor."""

    async def execute(self, query: str) -> list[tuple]:
        """Single method to execute query.

        Note that order of elements in tuple `must` be
        similar to columns in query SELECT statement
        if it has ones.

        Args:
            query (str): String that contains SQL query

        Returns:
            list[tuple]: List that contains result of query if it has result.
        """
        ...
