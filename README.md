# FastDTO

FastDTO is a Python [EdgeDB](https://www.edgedb.com/) inspired open source ORM framework designed to simplify database interactions by parsing user-defined SQL queries, generating Data Transfer Objects (DTOs), and creating Python functions to execute the queries and return the DTOs.

## Installation

You can install FastDTO via pip:

```sh
pip install fastdto
```

or poetry:

```sh
poetry add fastdto
```

## Getting started

First of all, you'll need to setup template directory as in [alembic](https://github.com/sqlalchemy/alembic) for working with your database schema and queries.
You easily can do it, via CLI command:

```sh
fastdto init
```

For now you should have something like this in your project directory:

```
YourProjectName/
├── dbschema/
│   ├── scripts/
│   │   ├──...
│   ├── dbschema.py
│   ├── README.md
...
```

In dbschema.py file you need to define your database schema, you can use README.md file, in section Schema for more definitive guide, how to do it, or check examples.

## Writing queries

Unlike other popular ORMs, in FastDTO, users describe SQL queries not in Python files using a query builder, but in pure SQL within separate `.sql` files. This is driven by the framework's philosophy to provide developers with complete freedom and control over SQL queries, shielding them from inefficient queries generated by query builders and other pitfalls of modern ORM frameworks.

Once you know the SQL query you need, you can create a file named `your_query_name.sql` in the `db/schema/scripts/` directory.

An example of your project directory structure will now look like this:

```
YourProjectName/
├── dbschema/
│   ├── scripts/
│   │   ├──your_query_name.sql
│   ├── dbschema.py
│   ├── README.md
...
```

## Generating functions


 Now begins the most enjoyable part of our work. After the arduous process of writing and debugging the SQL query, we are ready to wrap it in Python. For this, you will need to run just one CLI command:

```sh
fastdto generate
```

After these magic words, the framework will generate an __init__.py file in the `dbschema/scripts/` directory. This file will contain the ready-to-use DTOs and asynchronous Python functions.

As example, for this SQL query:

```sql
SELECT number, owner_id FROM cars
```

FastDTO will generate this pair DTO and function:

```python3
class MyQueryResult(FastDTOModel):
    number: int
    owner_id: int


async def my_query(
    executor: IAsyncExecutor,
) -> list[MyQueryResult]:
    result = await executor.execute(
        """
        SELECT cars.number AS number, cars.owner_id AS owner_id FROM cars AS cars
        """,
    )
    return [MyQueryResult.from_list(row) for row in result]
```

Let's break it down.

 1. `MyQueryResult` is [Pydantic](https://docs.pydantic.dev/latest/) BaseModel subclass with just one extra method `from_list`, defined by `FastDTOModel` class.
 2. `my_query` is a async Python function that takes our query and executes its in database.
 3. `IAsyncExecutor` - interface with 1 method - `execute`, provided by FastDTO. You can use predefined executors like SQLAlchemy or write one by yourself.

## Using functions

As for example, here the code snippet, how to use `my_query` function from above with SQLAlchemy:


```python3
import asyncio
from dbschema.scripts import my_query
from fastdto.connection.sqlalchemy import SqlAlchemyAsyncExecutor  # Predefined SQLAlchemy executor


async def main():
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(
        "postgresql+asyncpg://user:password@localhost:5432/test"
    )
    async with engine.connect() as conn:
        result = await my_query(
            executor=SqlAlchemyAsyncExecutor(conn),
        )
        print(result)
        # result = [MyQueryResult(number=1, owner_id=1), MyQueryResult(number=2, owner_id=2)]

asyncio.run(main())
```


## License

FastDTO is distributed under the [MIT license](https://opensource.org/license/MIT).
