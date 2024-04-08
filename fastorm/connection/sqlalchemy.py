from sqlalchemy import text
from sqlalchemy.ext.asyncio.engine import AsyncConnection

from fastorm.connection.interface import IAsyncExecutor


class SqlAlchemyAsyncExecutor(IAsyncExecutor):
    """Boilerplate for execution with sqlalchemy connection."""

    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def execute(self, query: str) -> list[tuple]:
        """Single method to execute query.

        Note that order of elements in tuple `must` be
        similar to columns in query SELECT statement
        if it has ones.

        SqlAlchemy specific executor, in order to use it,
        you can check example below:
        ```
        async with engine.connect() as conn:
            result = await some_generated_func(
                executor=SqlAlchemyAsyncExecutor(conn),
                * // your args here
            )
        ```

        Args:
            query (str): String that contains SQL query

        Returns:
            list[tuple]: List that contains result of query if it has result.
        """
        return (await self.connection.execute(text(query))).fetchall()
