import json
import os
from pathlib import Path
from typing import Any, Dict

import typer
from rich import print

APP_NAME = "predibase-sdk-app"
LOCAL_SETTINGS_NAME = ".predibase.json"

app = typer.Typer()


@app.command(help="Show global settings")
def show_global():
    settings = load_global_settings()
    print(settings)


@app.command(help="Show local settings")
def show_local():
    settings = load_local_settings()
    print(settings)


@app.command(help="Show local and global settings")
def show_all():
    settings = load_settings()
    print(settings)


@app.command(help="Set default repository name")
def set_repo(repository_name: str = typer.Argument(..., help="The model repository name")):
    _set_setting("repo", repository_name)


@app.command(help="Set default engine name")
def set_engine(engine_name: str = typer.Argument(..., help="The engine name")):
    _set_setting("engine", engine_name)


@app.command(help="Set api token")
def set_api_token(token: str = typer.Argument(..., help="The api token")):
    _set_setting("token", token)


@app.command(help="Set default endpoint url")
def set_endpoint(endpoint: str = typer.Argument(..., help="The endpoint url")):
    _set_setting("endpoint", endpoint)


def _set_setting(setting: str, value: Any):
    settings = load_global_settings()
    settings[setting] = value
    save_global_settings(settings)


def get_global_settings_path() -> Path:
    app_dir = typer.get_app_dir(APP_NAME)
    return Path(app_dir) / "settings.json"


def save_global_settings(settings: Dict[str, Any]):
    settings_path = get_global_settings_path()
    os.makedirs(settings_path.parent, exist_ok=True)
    with open(settings_path, "w") as f:
        json.dump(settings, f)


def load_global_settings() -> Dict[str, Any]:
    settings_path = get_global_settings_path()
    if settings_path.is_file():
        with open(settings_path) as f:
            return json.load(f)
    return {}


def save_local_settings(settings: Dict[str, Any]):
    settings_path = Path(LOCAL_SETTINGS_NAME)
    os.makedirs(settings_path.parent, exist_ok=True)
    with open(settings_path, "w") as f:
        json.dump(settings, f)


def load_local_settings() -> Dict[str, Any]:
    settings_path = Path(LOCAL_SETTINGS_NAME)
    if settings_path.is_file():
        with open(settings_path) as f:
            return json.load(f)
    return {}


def load_settings() -> Dict[str, Any]:
    local_settings = load_local_settings()
    global_settings = load_global_settings()
    return {**global_settings, **local_settings}
