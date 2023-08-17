import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, TYPE_CHECKING, Union

import yaml
from dataclasses_json import config, dataclass_json, LetterCase

from predibase.resource.connection import get_dataset
from predibase.resource.dataset import Dataset
from predibase.resource.engine import Engine
from predibase.resource.llm.response import GeneratedResponse
from predibase.resource.model import create_model_repo, ModelFuture, ModelRepo
from predibase.util import load_yaml

if TYPE_CHECKING:
    from predibase.pql.api import Session


_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_TEMPLATE_DIR = os.path.join(_PATH_HERE, "templates")


class HuggingFaceLLM:
    def __init__(self, session: "Session", model_name: str):
        self.session = session
        self.model_name = model_name

    def deploy(
        self,
        deployment_name: str,
        engine_template: Optional[str] = None,
        scale_down_period=3600,
    ) -> "LLMDeployment":
        valid_llms = self.session.get_json("/supported_llms")
        valid_llms_by_names = {x["modelName"]: x for x in valid_llms}
        if self.model_name not in valid_llms_by_names:
            raise ValueError(
                f"Model name {self.model_name} is not supported. Valid models are: {valid_llms_by_names.keys()}",
            )

        model_params = {
            **valid_llms_by_names[self.model_name],
            "name": deployment_name,
            "modelName": self.model_name,
            "engineTemplate": engine_template,
            "scaleDownPeriod": scale_down_period,
        }
        print("Deploying the model with the following params:")
        print(model_params)

        self.session.post_json(
            "/llms",
            json=model_params,
        )

        self.session.post_json(
            "/llms",
            json={
                "name": deployment_name,
                "modelName": self.model_name,
                "engineTemplate": engine_template,
                "scaleDownPeriod": scale_down_period,
            },
        )

    def finetune(
        self,
        template: Optional[str] = None,
        target: Optional[str] = None,
        dataset: Optional[Union[str, Dataset]] = None,
        engine: Optional[Union[str, Engine]] = None,
        config: Optional[Union[str, Dict]] = None,
        repo: Optional[str] = None,
    ) -> ModelFuture:
        if config is None:
            with open(os.path.join(_TEMPLATE_DIR, "defaults.yaml")) as f:
                config_str = f.read()
            config_str = config_str.format(base_model=self.model_name, template=template, target=target)
            config = yaml.safe_load(config_str)
        else:
            config = load_yaml(config)

        if repo is None:
            dataset_name = dataset.name if isinstance(dataset, Dataset) else dataset
            repo = f"{self.model_name}-{dataset_name}"

        repo: ModelRepo = get_or_create_repo(self.session, repo)
        if dataset is None:
            # Assume the dataset is the same as the repo head
            md = repo.head().to_draft()
            md.config = config
        else:
            if isinstance(dataset, str):
                conn_name = None
                if "/" in dataset:
                    conn_name, dataset = dataset.split("/")
                dataset = get_dataset(self.session, dataset, connection_name=conn_name)
            md = repo.create_draft(config=config, dataset=dataset)

        return md.train_async(engine=engine)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class _LLMDeployment:
    id: int = field(metadata=config(field_name="id"))
    tenant_id: int = field(metadata=config(field_name="tenantID"))
    uuid: str = field(metadata=config(field_name="uuid"))
    name: str = field(metadata=config(field_name="name"))
    description: Optional[str] = field(metadata=config(field_name="description"))
    model_name: str = field(metadata=config(field_name="modelName"))
    num_shards: Optional[int] = field(metadata=config(field_name="num_shards"))
    quantize: bool = field(metadata=config(field_name="quantize"))
    deployment_status: str = field(metadata=config(field_name="deploymentStatus"))

    prompt_template: str = field(metadata=config(field_name="promptTemplate"))
    min_replicas: int = field(metadata=config(field_name="minReplicas"))
    max_replicas: int = field(metadata=config(field_name="maxReplicas"))
    created: str = field(metadata=config(field_name="created"))
    updated: str = field(metadata=config(field_name="updated"))
    created_by_user_id: Optional[int] = field(metadata=config(field_name="createdByUserID"))
    scale_down_period: int = field(metadata=config(field_name="scaleDownPeriod"))


class LLMDeployment:
    def __init__(self, session: "Session", model_name: str):
        self.session = session
        self.model_name = model_name
        self.data = _LLMDeployment.from_dict(self.session.get_json(f"/llms/{self.model_name}"))

    def prompt(
        self,
        templates: Union[str, List[str]],
        index: Optional[Union[str, Dataset]] = None,
        dataset: Optional[Union[str, Dataset]] = None,
        limit: Optional[int] = None,
        options: Optional[Dict[str, float]] = None,
    ) -> List[GeneratedResponse]:
        resp = self.session.post_json(
            "/prompt",
            json={
                "model_name": [self.model_name],
                "templates": [templates] if isinstance(templates, str) else templates,
                "options": options,
                "limit": limit,
                "index_name": index.name if isinstance(index, Dataset) else index,
                "dataset_name": dataset.name if isinstance(dataset, Dataset) else dataset,
            },
        )

        responses = resp["responses"]
        return [GeneratedResponse(**r) for r in responses]


def get_or_create_repo(session: "Session", repo_name: str) -> ModelRepo:
    return create_model_repo(session, name=repo_name, exists_ok=True)
