from typing import Type
from functools import lru_cache
import urllib.parse
import requests
from xia_engine import BaseDocument
from xia_engine import Engine
from xia_gpt_engine_gitlab.engine import GitlabEngineParam, GitlabEngineClient


class GitlabWikiEngineClient(GitlabEngineClient):
    def create_wiki(self, project_name: str, wiki_path: str, wiki_content: str):
        """Create wiki page

        Args:
            project_name: Project name
            wiki_path: document id
            wiki_content: database content
        """
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        wiki_endpoint = f"{self.api_endpoint}/projects/{project_id}/wikis"
        payload = {"title": wiki_path, "content": wiki_content}
        response = requests.post(wiki_endpoint, headers=self.api_headers, data=payload)
        self.check_response(response)

    def update_wiki(self, project_name: str, wiki_path: str, wiki_content: str):
        """Update wiki page

        Args:
            project_name: Project name
            wiki_path: document id
            wiki_content: database content
        """
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        wiki_endpoint = f"{self.api_endpoint}/projects/{project_id}/wikis/{urllib.parse.quote(wiki_path, safe='')}"
        payload = {"title": wiki_path, "content": wiki_content}
        response = requests.put(wiki_endpoint, headers=self.api_headers, data=payload)
        self.check_response(response)

    def get_wiki(self, project_name: str, wiki_path: str):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        wiki_endpoint = f"{self.api_endpoint}/projects/{project_id}/wikis/{urllib.parse.quote(wiki_path, safe='')}"
        response = requests.get(wiki_endpoint, headers=self.api_headers)
        if response.status_code == 200:
            return response.json()["content"]
        return ""

    def delete_wiki(self, project_name: str, wiki_path: str):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        wiki_endpoint = f"{self.api_endpoint}/projects/{project_id}/wikis/{urllib.parse.quote(wiki_path, safe='')}"
        response = requests.delete(wiki_endpoint, headers=self.api_headers)
        if 200 <= response.status_code < 300:
            return True
        return False


class GitlabWikiEngine(Engine):
    """XIA Document Engine based on Gitlab Wiki Pages
    """
    engine_param = "gitlab_wiki"
    engine_connector_class = GitlabEngineParam
    engine_connector = GitlabWikiEngineClient

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None) -> str:
        db_con = cls.get_connection(document_class)
        project_name = db_content["target"]
        wiki_path = db_content["key"]
        wiki_content = db_content["value"]
        db_con.create_wiki(project_name, wiki_path, wiki_content)
        return doc_id

    @classmethod
    def get(cls, document_class: Type[BaseDocument], doc_id: str) -> dict:
        db_con = cls.get_connection(document_class)
        doc_dict = document_class.id_to_dict(doc_id)
        doc_dict["value"] = db_con.get_wiki(doc_dict["target"], doc_dict["key"])
        doc_dict["_id"] = doc_id
        return doc_dict if doc_dict["value"] else {}

    @classmethod
    def set(cls, document_class: Type[BaseDocument], doc_id: str, db_content: dict) -> str:
        db_con = cls.get_connection(document_class)
        doc_dict = document_class.id_to_dict(doc_id)
        db_con.update_wiki(doc_dict["target"], doc_dict["key"], db_content["value"])
        return doc_id

    @classmethod
    def update(cls, _document_class: Type[BaseDocument], _doc_id: str, **kwargs) -> dict:
        db_con = cls.get_connection(_document_class)
        doc_dict = _document_class.id_to_dict(_doc_id)
        db_con.update_wiki(doc_dict["target"], doc_dict["key"], kwargs["value"])
        return cls.get(_document_class, _doc_id)

    @classmethod
    def fetch(cls, document_class: Type[BaseDocument], *args):
        db_con = cls.get_connection(document_class)
        for doc_id in args:
            doc_dict = document_class.id_to_dict(doc_id)
            doc_dict["value"] = db_con.get_wiki(doc_dict["target"], doc_dict["key"])
            doc_dict["_id"] = doc_id
            if doc_dict["value"]:
                yield doc_id, doc_dict

    @classmethod
    def delete(cls, document_class: Type[BaseDocument], doc_id: str):
        db_con = cls.get_connection(document_class)
        old_data = cls.get(document_class, doc_id)
        if not old_data:
            return
        doc_dict = document_class.id_to_dict(doc_id)
        db_con.delete_wiki(doc_dict["target"], doc_dict["key"])
