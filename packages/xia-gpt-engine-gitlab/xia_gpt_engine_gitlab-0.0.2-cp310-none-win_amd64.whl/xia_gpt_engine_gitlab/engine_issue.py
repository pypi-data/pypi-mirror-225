import json
from typing import Type
from functools import lru_cache
import urllib.parse
import requests
from xia_engine import BaseDocument
from xia_gpt_engine_gitlab.engine import GitlabEngineParam, GitlabEngineClient, GitlabEngine
from xia_gpt_engine_gitlab.engine_milestone import GitlabMilestoneEngineClient


class GitlabIssueEngineClient(GitlabEngineClient):
    @classmethod
    @lru_cache(maxsize=2048)
    def get_issue_iid_from_name(cls, api_endpoint: str, api_token: str, project_id: int, issue_name: str) -> int:
        params = {"search": issue_name}
        headers = {"PRIVATE-TOKEN": api_token}
        response = requests.get(f"{api_endpoint}/projects/{project_id}/issues", headers=headers, params=params)
        if response.status_code == 200:
            for issue in response.json():
                if issue["title"] == issue_name:
                    return issue["iid"]

    def create_issue(self, project_name: str, issue_name: str, issue_content: str, **kwargs):
        """Create issue page

        Args:
            project_name: Project name
            issue_name: Issue Name
            issue_content: database content
        """
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_endpoint = f"{self.api_endpoint}/projects/{project_id}/issues"
        payload = {"title": issue_name, "description": issue_content}
        response = requests.post(issue_endpoint, headers=self.api_headers, data=payload)
        self.check_response(response)
        self.get_issue_iid_from_name.cache_clear()  # Need to clear cache to reflecting new issues

    def update_issue(self, project_name: str, issue_name: str, issue_content: str, state_event: str = "", **kwargs):
        """Update issue page

        Args:
            project_name: Project name
            issue_name: document id
            issue_content: database content
            state_event: change event, should be one of "close", "reopen"
        """
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_iid = self.get_issue_iid_from_name(self.api_endpoint, self.api_token, project_id, issue_name)
        issue_endpoint = f"{self.api_endpoint}/projects/{project_id}/issues/{issue_iid}"
        payload = {"title": issue_name, "description": issue_content}
        if state_event in ["close", "reopen"]:
            payload["state_event"] = state_event
        response = requests.put(issue_endpoint, headers=self.api_headers, data=payload)
        self.check_response(response)

    def get_issue(self, project_name: str, issue_name: str, **kwargs):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_iid = self.get_issue_iid_from_name(self.api_endpoint, self.api_token, project_id, issue_name)
        issue_endpoint = f"{self.api_endpoint}/projects/{project_id}/issues/{issue_iid}"
        response = requests.get(issue_endpoint, headers=self.api_headers)
        if response.status_code == 200:
            return response.json()["description"]
        return {}

    def delete_issue(self, project_name: str, issue_name: str, **kwargs):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_iid = self.get_issue_iid_from_name(self.api_endpoint, self.api_token, project_id, issue_name)
        issue_endpoint = f"{self.api_endpoint}/projects/{project_id}/issues/{issue_iid}"
        response = requests.delete(issue_endpoint, headers=self.api_headers)
        if 200 <= response.status_code < 300:
            self.get_issue_iid_from_name.cache_clear()  # Need to clear cache
            return True
        return False


class GitlabIssueEngine(GitlabEngine):
    """XIA Document Engine based on Gitlab Issues
    """
    engine_param = "gitlab_issue"
    engine_connector_class = GitlabEngineParam
    engine_connector = GitlabIssueEngineClient

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None) -> str:
        db_con = cls.get_connection(document_class)
        project_name = db_content["target"]
        issue_name = db_content["name"]
        issue_content = cls.db_to_content(document_class, db_content)
        db_con.create_issue(project_name, issue_name, issue_content)
        return doc_id

    @classmethod
    def get(cls, document_class: Type[BaseDocument], doc_id: str) -> dict:
        db_con = cls.get_connection(document_class)
        doc_dict = document_class.id_to_dict(doc_id)
        issue_content = db_con.get_issue(doc_dict["target"], doc_dict["name"])
        if not issue_content:
            return {}  # No data found
        doc_data = cls.content_to_dict(document_class, issue_content)
        doc_dict.update(doc_data)
        doc_dict["_id"] = doc_id
        return doc_dict

    @classmethod
    def set(cls, document_class: Type[BaseDocument], doc_id: str, db_content: dict) -> str:
        db_con = cls.get_connection(document_class)
        doc_dict = document_class.id_to_dict(doc_id)
        milestone_content = cls.db_to_content(document_class, db_content)
        db_con.update_issue(doc_dict["target"], doc_dict["name"], milestone_content)
        return doc_id

    @classmethod
    def update(cls, _document_class: Type[BaseDocument], _doc_id: str, **kwargs) -> dict:
        state_map = {("closed", "opened"): "reopen", ("opened", "closed"): "close"}
        db_con = cls.get_connection(_document_class)
        doc_dict = _document_class.id_to_dict(_doc_id)
        issue_content = db_con.get_issue(doc_dict["target"], doc_dict["name"])
        doc_data = cls.content_to_dict(_document_class, issue_content)
        doc_dict.update(doc_data)
        doc_dict.update(**kwargs)
        state_event = state_map.get((doc_data.get("status", ""), kwargs.get("status", "")), "")
        issue_content = cls.db_to_content(_document_class, doc_dict)
        db_con.update_issue(doc_dict["target"], doc_dict["name"], issue_content, state_event)
        return cls.get(_document_class, _doc_id)

    @classmethod
    def fetch(cls, document_class: Type[BaseDocument], *args):
        db_con = cls.get_connection(document_class)
        for doc_id in args:
            doc_dict = document_class.id_to_dict(doc_id)
            issue_content = db_con.get_issue(doc_dict["target"], doc_dict["name"])
            if issue_content:
                doc_data = cls.content_to_dict(document_class, issue_content)
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
        db_con.delete_issue(doc_dict["target"], doc_dict["name"])


class GitlabSubIssueEngineClient(GitlabIssueEngineClient):
    """Issue management with parent node"""
    def create_sub_issue(self, project_name: str, parent_name: str, issue_name: str, issue_content: str, **kwargs):
        pass


class GitlabMilestoneIssueEngineClient(GitlabSubIssueEngineClient):
    """Issue management with Milestone as parent node"""
    def create_sub_issue(self, project_name: str, parent_name: str, issue_name: str, issue_content: str, **kwargs):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        milestone_id = GitlabMilestoneEngineClient.get_milestone_id_from_name(self.api_endpoint, self.api_token,
                                                                              project_id, parent_name)
        if not milestone_id:
            raise ValueError(f"Milestone {parent_name} cannot be found on Project {project_name}")
        issue_endpoint = f"{self.api_endpoint}/projects/{project_id}/issues"
        payload = {"title": issue_name, "description": issue_content, "milestone_id": milestone_id}
        response = requests.post(issue_endpoint, headers=self.api_headers, data=payload)
        self.check_response(response)
        self.get_issue_iid_from_name.cache_clear()  # Need to clear cache to reflecting new issues


class GitlabMilestoneIssueEngine(GitlabIssueEngine):
    """XIA Document Engine based on Gitlab Issues with parents
    """
    engine_param = "gitlab_milestone_issue"
    engine_connector_class = GitlabEngineParam
    engine_connector = GitlabMilestoneIssueEngineClient

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None) -> str:
        db_con = cls.get_connection(document_class)
        project_name = db_content["target"]
        parent_name = db_content["campaign"]
        issue_name = db_content["name"]
        issue_content = cls.db_to_content(document_class, db_content)
        db_con.create_sub_issue(project_name, parent_name, issue_name, issue_content)
        return doc_id
