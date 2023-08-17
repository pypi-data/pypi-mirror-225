import re
from typing import Optional

import typer

from predibase.cli_commands.utils import get_client, get_console

app = typer.Typer()


# TODO(travis): this should be dynamic based on model type and pushed to the backend
DEFAULT_TEMPLATE = "llm-gpu-small"


@app.command(help="Create a Large Language Model (LLM) deployment")
def llm(
    deployment_name: str = typer.Option(
        None,
        "--deployment-name",
        "-d",
        prompt="Deployment name",
        prompt_required=True,
        help="Name of the deployment",
    ),
    model_name: str = typer.Option(
        None,
        "--model-name",
        "-m",
        prompt="Model to deploy",
        prompt_required=True,
        help="Name of the model",
    ),
    engine_template: Optional[str] = typer.Option(
        DEFAULT_TEMPLATE,
        "--engine-template",
        "-e",
        prompt="Engine name",
        prompt_required=False,
        help="Optional engine template to provision for hosting the model",
    ),
    auto_suspend_secs: Optional[int] = 3600,
):
    # raise ValueError if name is not lower case alphanumeric characters or '-'
    if re.match(r"^[a-z0-9-]+$", deployment_name) is None:
        raise ValueError("name must be lower case alphanumeric characters or '-'")

    client = get_client()

    get_console().print("Deploying an LLM with the following parameters:")
    get_console().print("\tdeployment_name:", deployment_name)
    get_console().print("\tmodel_name:", model_name)
    get_console().print("\tengine_template:", engine_template)
    get_console().print("\tauto_suspend_secs:", auto_suspend_secs)

    client.deploy_llm(
        deployment_name,
        model_name,
        engine_template=engine_template,
        scale_down_period=auto_suspend_secs,
    )
    get_console().print("Deploy request sent.")


if __name__ == "__main__":
    app()
