from typer import Argument, Typer

from fastorm.core.codegen.service import init_project_structure

app = Typer()


@app.command()
def init(directory: str = Argument(default="dbschema")):  # noqa: B008
    """Generates file structure for DB schema and scripts.

    Args:
        directory (str, optional): Specify directory of project.
            Defaults to "dbschema".
    """
    init_project_structure(directory=directory)
