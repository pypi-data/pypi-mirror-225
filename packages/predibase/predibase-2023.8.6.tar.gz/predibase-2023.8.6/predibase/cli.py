from typing import Optional

import typer

# from predibase.cli_commands import run
from predibase.cli_commands import create, delete, deploy, list_resources, prompt, settings
from predibase.cli_commands.utils import set_defaults_from_settings
from predibase.util.settings import load_settings, save_global_settings, save_local_settings

app = typer.Typer(help="Predibase CLI commands")

app.add_typer(create.app, name="create", help="Create Predibase resources")
app.add_typer(deploy.app, name="deploy", help="Deploy Predibase resources")
app.add_typer(delete.app, name="delete", help="Delete Predibase resources")
app.add_typer(list_resources.app, name="list", help="List Predibase resources")
app.add_typer(prompt.app, name="prompt", help="Prompt Predibase models")
app.add_typer(settings.app, name="settings", help="Configure Predibase settings")


@app.command(help="Initialize Predibase with API token")
def init(
    token: Optional[str] = typer.Option(
        None,
        "--token",
        "-t",
        help="The optional api token",
        prompt="API Token",
    ),
):
    save_global_settings({k: v for k, v in dict(token=token).items() if v})


@app.command(help="Initialize local default model repository and engine")
def init_local(
    repository_name: Optional[str] = typer.Option(
        None,
        "--repository-name",
        "-r",
        help="The optional model repository name",
    ),
    engine_name: Optional[str] = typer.Option(None, "--engine-name", "-e", help="The optional engine name"),
    quiet: bool = False,
):
    save_local_settings({k: v for k, v in dict(repo=repository_name or "", engine=engine_name or "").items() if v})


@app.command(help="Train a new model from a Ludwig config")
def train(
    config: Optional[str] = None,
    dataset: Optional[str] = None,
    repo: Optional[str] = None,
    engine: Optional[str] = None,
    message: Optional[str] = typer.Option(None, "--message", "-m"),
    watch: bool = False,
):
    create.model(config, dataset, repo, engine, message, watch)


def main():
    set_defaults_from_settings(load_settings())
    app()


if __name__ == "__main__":
    main()
