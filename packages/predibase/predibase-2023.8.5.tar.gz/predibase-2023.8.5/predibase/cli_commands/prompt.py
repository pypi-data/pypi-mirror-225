from typing import Optional

import pandas as pd
import typer
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from predibase.cli_commands.utils import get_client, get_console

app = typer.Typer()


@app.command(help="Query a Large Language Model (LLM)")
def llm(
    template: str = typer.Option(
        None,
        "--template",
        "-t",
        prompt="Template input",
        prompt_required=True,
        help="Prompt template input text",
    ),
    model_name: str = typer.Option(
        None,
        "--model-name",
        "-m",
        prompt="Model to query",
        prompt_required=True,
        help="Name of the model",
    ),
    index_name: Optional[str] = typer.Option(
        None,
        "--index-name",
        "-i",
        prompt_required=False,
        help="Optional dataset to index",
    ),
    dataset_name: Optional[str] = typer.Option(
        None,
        "--dataset-name",
        "-d",
        prompt_required=False,
        help="Optional dataset for batch inference",
    ),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", prompt_required=False, help="Optional results limit"),
):
    client = get_client()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Querying LLM...", total=None)

        df = client.prompt(
            template,
            model_name,
            index=index_name,
            dataset=dataset_name,
            limit=limit,
            return_df=True,
        )

    table = Table(show_header=True, header_style="bold magenta")

    # Modify the table instance to have the data from the DataFrame
    table = df_to_table(df, table)

    # Update the style of the table
    table.row_styles = ["none", "dim"]
    table.box = box.SIMPLE_HEAD

    get_console().print(table)


def df_to_table(
    pandas_dataframe: pd.DataFrame,
    rich_table: Table,
    show_index: bool = True,
    index_name: Optional[str] = None,
) -> Table:
    """Convert a pandas.DataFrame obj into a rich.Table obj.

    Args:
        pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
        rich_table (Table): A rich Table that should be populated by the DataFrame values.
        show_index (bool): Add a column with a row count to the table. Defaults to True.
        index_name (str, optional): The column name to give to the index column. Defaults to None, showing no value.
    Returns:
        Table: The rich Table instance passed, populated with the DataFrame values.
    """

    if show_index:
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in pandas_dataframe.columns:
        rich_table.add_column(str(column))

    for index, value_list in enumerate(pandas_dataframe.values.tolist()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list]
        rich_table.add_row(*row)

    return rich_table


if __name__ == "__main__":
    app()
