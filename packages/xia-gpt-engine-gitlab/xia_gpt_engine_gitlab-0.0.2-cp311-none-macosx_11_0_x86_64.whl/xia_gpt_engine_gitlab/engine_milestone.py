import json
from typing import Type
from functools import lru_cache
import urllib.parse
import requests
from xia_engine import BaseDocument
from xia_gpt_engine_gitlab.engine import GitlabEngineParam, GitlabEngineClient, GitlabEngine


class GitlabMilestoneEngineClient(GitlabEngineClient):
    @classmethod
    @lru_cache(maxsize=2048)
    def get_milestone_id_from_name(cls, api_endpoint: str, api_token: str, project_id: int, milestone_name: str) -> int:
        params = {"title": milestone_name}
        headers = {"PRIVATE-TOKEN": api_token}
        response = requests.get(f"{api_endpoint}/projects/{project_id}/milestones", headers=headers, params=params)
        if response.status_code == 200:
            for milestone in response.json():
                if milestone["title"] == milestone_name:
                    return milestone["id"]

    def create_milestone(self, project_name: str, milestone_name: str, milestone_content: str):
        """Create milestone page

        Args:
            project_name: Project name
            milestone_name: Issue Name
            milestone_content: database content
        """
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        milestone_endpoint = f"{self.api_endpoint}/projects/{project_id}/milestones"
        payload = {"title": milestone_name, "description": milestone_content}
        response = requests.post(milestone_endpoint, headers=self.api_headers, data=payload)
        self.check_response(response)
        self.get_milestone_id_from_name.cache_clear()  # Need to clear cache to reflecting new milestones

    def update_milestone(self, project_name: str, milestone_name: str, milestone_content: str, state_event: str = "",
                         **kwargs):
        """Update milestone page

        Args:
            project_name: Project name
            milestone_name: document id
            milestone_content: database content
            state_event: change event, should be one of "close", "activate"
        """
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        milestone_iid = self.get_milestone_id_from_name(self.api_endpoint, self.api_token, project_id, milestone_name)
        milestone_endpoint = f"{self.api_endpoint}/projects/{project_id}/milestones/{milestone_iid}"
        payload = {"title": milestone_name, "description": milestone_content}
        if state_event in ["close", "activate"]:
            payload["state_event"] = state_event
        response = requests.put(milestone_endpoint, headers=self.api_headers, data=payload)
        self.check_response(response)

    def get_milestone(self, project_name: str, milestone_name: str):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        milestone_iid = self.get_milestone_id_from_name(self.api_endpoint, self.api_token, project_id, milestone_name)
        milestone_endpoint = f"{self.api_endpoint}/projects/{project_id}/milestones/{milestone_iid}"
        response = requests.get(milestone_endpoint, headers=self.api_headers)
        if response.status_code == 200:
            return response.json()["description"]
        return {}

    def delete_milestone(self, project_name: str, milestone_name: str):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        milestone_iid = self.get_milestone_id_from_name(self.api_endpoint, self.api_token, project_id, milestone_name)
        milestone_endpoint = f"{self.api_endpoint}/projects/{project_id}/milestones/{milestone_iid}"
        response = requests.delete(milestone_endpoint, headers=self.api_headers)
        if 200 <= response.status_code < 300:
            self.get_milestone_id_from_name.cache_clear()  # Need to clear cache
            return True
        return False


class GitlabMilestoneEngine(GitlabEngine):
    """XIA Document Engine based on Gitlab Issues
    """
    engine_param = "gitlab_milestone"
    engine_connector_class = GitlabEngineParam
    engine_connector = GitlabMilestoneEngineClient

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None) -> str:
        db_con = cls.get_connection(document_class)
        project_name = db_content["target"]
        milestone_name = db_content["name"]
        milestone_content = cls.db_to_content(document_class, db_content)
        db_con.create_milestone(project_name, milestone_name, milestone_content)
        return doc_id

    @classmethod
    def get(cls, document_class: Type[BaseDocument], doc_id: str) -> dict:
        db_con = cls.get_connection(document_class)
        doc_dict = document_class.id_to_dict(doc_id)
        milestone_content = db_con.get_milestone(doc_dict["target"], doc_dict["name"])
        if not milestone_content:
            return {}  # No data found
        doc_data = cls.content_to_dict(document_class, milestone_content)
        doc_dict.update(doc_data)
        doc_dict["_id"] = doc_id
        return doc_dict

    @classmethod
    def set(cls, document_class: Type[BaseDocument], doc_id: str, db_content: dict) -> str:
        db_con = cls.get_connection(document_class)
        doc_dict = document_class.id_to_dict(doc_id)
        milestone_content = cls.db_to_content(document_class, db_content)
        db_con.update_milestone(doc_dict["target"], doc_dict["name"], milestone_content)
        return doc_id

    @classmethod
    def update(cls, _document_class: Type[BaseDocument], _doc_id: str, **kwargs) -> dict:
        state_map = {("closed", "opened"): "activate", ("opened", "closed"): "close"}
        db_con = cls.get_connection(_document_class)
        doc_dict = _document_class.id_to_dict(_doc_id)
        milestone_content = db_con.get_milestone(doc_dict["target"], doc_dict["name"])
        doc_data = cls.content_to_dict(_document_class, milestone_content)
        doc_dict.update(doc_data)
        doc_dict.update(**kwargs)
        state_event = state_map.get((doc_data.get("status", ""), kwargs.get("status", "")), "")
        milestone_content = cls.db_to_content(_document_class, doc_dict)
        db_con.update_milestone(doc_dict["target"], doc_dict["name"], milestone_content, state_event)
        return cls.get(_document_class, _doc_id)

    @classmethod
    def fetch(cls, document_class: Type[BaseDocument], *args):
        db_con = cls.get_connection(document_class)
        for doc_id in args:
            doc_dict = document_class.id_to_dict(doc_id)
            milestone_content = db_con.get_milestone(doc_dict["target"], doc_dict["name"])
            if milestone_content:
                doc_data = cls.content_to_dict(document_class, milestone_content)
                doc_dict.update(doc_data)
                doc_dict["_id"] = doc_id
                yield doc_id, doc_dict

    @classmethod
    def delete(cls, document_class: Type[BaseDocument], doc_id: str):
        db_con = cls.get_connection(document_class)
        old_data = cls.get(document_class, doc_id)
        if not old_data:
            return
        doc_dict = document_class.id_to_dict(doc_id)
        db_con.delete_milestone(doc_dict["target"], doc_dict["name"])
