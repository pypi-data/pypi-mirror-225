from dataclasses import dataclass
from typing import Any, Dict, Optional

import yaml
from rich.console import Console

from predibase import PredibaseClient
from predibase.pql.api import Session
from predibase.resource.dataset import Dataset
from predibase.resource.engine import Engine
from predibase.resource.model import ModelRepo


@dataclass
class Defaults:
    repo: Optional[str] = None
    engine: Optional[str] = None
    session: Optional[Session] = None


console = Console()
defaults: Defaults = Defaults()


def get_console() -> Console:
    return console


def get_client() -> PredibaseClient:
    return PredibaseClient(session=defaults.session)


def sanitize_engine_name(name: str) -> str:
    return name.replace("/", "-")


def get_or_create_repo(repo_name: Optional[str] = None) -> ModelRepo:
    repo_name = repo_name or defaults.repo
    if repo_name is None:
        raise ValueError("Repo name is required")
    return get_client().create_model_repo(name=repo_name, exists_ok=True)


def get_repo(repo_name: Optional[str] = None) -> ModelRepo:
    repo_name = repo_name or defaults.repo
    if repo_name is None:
        raise ValueError("Repo name is required")
    return get_client().get_model_repo(name=repo_name)


def get_engine(engine_name: Optional[str] = None) -> Engine:
    engine_name = engine_name or defaults.engine
    if engine_name is None:
        raise ValueError("Engine name is required")
    return get_client().get_engine(name=engine_name)


def get_dataset(dataset_name: Optional[str] = None) -> Dataset:
    if dataset_name is None:
        raise ValueError("Dataset name is required")

    conn_name = None
    if "/" in dataset_name:
        conn_name, dataset_name = dataset_name.split("/")
    return get_client().get_dataset(dataset_name=dataset_name, connection_name=conn_name)


def set_defaults_from_settings(settings: Dict[str, Any]):
    global defaults
    defaults = Defaults(
        repo=settings.get("repo"),
        engine=settings.get("engine"),
        session=Session(token=settings.get("token"), url=settings.get("endpoint")),
    )


def load_yaml(fname: str) -> Dict[str, Any]:
    with open(fname) as f:
        return yaml.safe_load(f)
