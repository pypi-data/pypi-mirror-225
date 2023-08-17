from typing import Type
from functools import lru_cache
import yaml
import requests
from xia_fields import StringField, OsEnvironField, IntField
from xia_engine import BaseDocument, EmbeddedDocument, Engine


class GitlabEngineParam(EmbeddedDocument):
    api_host: str = StringField(description="Gitlab API HOST")
    api_token: str = OsEnvironField(desription="Gitlab Access Token", prefix="GITLAB_", required=True)
    resource_type: str = StringField(description="Resource Type", choices=["projects", "groups"], required=True)
    resource_id: int = IntField(description="Resource ID")


class GitlabEngineClient:
    @classmethod
    @lru_cache(maxsize=2048)
    def get_project_id_from_name(cls, api_endpoint: str, api_token: str, project_name: str) -> int:
        params = {"search": project_name}
        headers = {"PRIVATE-TOKEN": api_token}
        response = requests.get(api_endpoint + "/projects", headers=headers, params=params)
        if response.status_code == 200:
            for project in response.json():
                if project["path"] == project_name:
                    return project["id"]

    def __init__(self, api_host: str, api_token: str, **kwargs):
        self.api_host = api_host
        self.api_token = api_token
        self.api_endpoint = f"https://{api_host}/api/v4"
        self.api_headers = {'PRIVATE-TOKEN': self.api_token}
        self.extra_params = kwargs

    def check_response(self, response):
        if 200 <= response.status_code < 300:
            return
        elif response.status_code == 400:
            raise ValueError(response.content.decode())
        else:
            raise RuntimeError(response.content.decode())


class GitlabEngine(Engine):
    """Gitlab Engine base, shouldn't be directly used"""
    engine_connector_class = GitlabEngineParam

    @classmethod
    def content_to_dict(cls, document_class: Type[BaseDocument], content: str) -> dict:
        if not content.startswith("```yaml\n") or not content.endswith("\n```"):
            return {}  # Format error
        display_data = yaml.load(content[8:-4], Loader=yaml.FullLoader)
        internal_data = document_class.from_display(**display_data).get_raw_data()
        return {k: v for k, v in internal_data.items() if k not in document_class._key_fields}

    @classmethod
    def db_to_content(cls, document_class: Type[BaseDocument], db_content: dict):
        dict_content = document_class.from_db(**db_content).get_display_data()
        dict_content = {k: v for k, v in dict_content.items()
                        if k not in document_class._key_fields and k in db_content}
        yaml_content = yaml.dump(dict_content, default_flow_style=False)
        return f"```yaml\n{yaml_content}\n```"
