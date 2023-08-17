from typing import Type
from functools import lru_cache
import urllib.parse
import requests
from xia_engine import BaseDocument
from xia_engine import Engine
from xia_gpt_engine_gitlab.engine import GitlabEngineParam, GitlabEngineClient, GitlabEngine
from xia_gpt_engine_gitlab.engine_issue import GitlabIssueEngineClient


class GitlabDiscussionEngineClient(GitlabEngineClient):
    def create_discussion(self, project_name: str, parent_name: str, discussion_content: str):
        """Create discussion page

        Args:
            project_name: Project name
            parent_name: Parent name which could hold the discussion
            discussion_content: database content
        """

    def get_discussion(self, project_name: str, parent_name: str, discussion_id: str):
        """Update discussion page

        Args:
            project_name: Project name
            parent_name: Parent name which could hold the discussion
            discussion_id: Discussion ID
        """

    def update_discussion(self, project_name: str, parent_name: str, discussion_id: str, discussion_content: str):
        """Update discussion

        Args:
            project_name: Project name
            parent_name: Parent name which could hold the discussion
            discussion_id: Discussion ID
            discussion_content: Discussion Content
        """


class GitlabIssueDiscussionEngineClient(GitlabDiscussionEngineClient):
    @classmethod
    @lru_cache(maxsize=2048)
    def get_discussion_note_id(cls, api_endpoint: str, api_token: str, project_id: int,
                               issue_iid: int, discussion_id: str) -> int:
        headers = {"PRIVATE-TOKEN": api_token}
        response = requests.get(f"{api_endpoint}/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}",
                                headers=headers)
        if response.status_code == 200:
            return response.json()["notes"][0]["id"]

    def create_discussion(self, project_name: str, parent_name: str, discussion_content: str):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_iid = GitlabIssueEngineClient.get_issue_iid_from_name(self.api_endpoint, self.api_token, project_id,
                                                                    parent_name)
        discussion_url = f"{self.api_endpoint}/projects/{project_id}/issues/{issue_iid}/discussions"
        payload = {"body": discussion_content}
        response = requests.post(discussion_url, headers=self.api_headers, data=payload)
        self.check_response(response)
        return response.json()

    def update_discussion(self, project_name: str, parent_name: str, discussion_id: str, discussion_content: str):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_iid = GitlabIssueEngineClient.get_issue_iid_from_name(self.api_endpoint, self.api_token, project_id,
                                                                    parent_name)
        note_id = self.get_discussion_note_id(self.api_endpoint, self.api_token, project_id, issue_iid, discussion_id)
        note_url = f"{self.api_endpoint}/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}/" \
                   f"notes/{note_id}"
        payload = {"body": discussion_content}
        response = requests.put(note_url, headers=self.api_headers, data=payload)
        self.check_response(response)

    def get_discussion(self, project_name: str, parent_name: str, discussion_id: str):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_iid = GitlabIssueEngineClient.get_issue_iid_from_name(self.api_endpoint, self.api_token, project_id,
                                                                    parent_name)
        discussion_url = f"{self.api_endpoint}/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}"
        response = requests.get(discussion_url, headers=self.api_headers)
        if response.status_code == 200:
            return response.json()["notes"][0]["body"]
        return ""

    def delete_discussion(self, project_name: str, parent_name: str, discussion_id: int):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_iid = GitlabIssueEngineClient.get_issue_iid_from_name(self.api_endpoint, self.api_token, project_id,
                                                                    parent_name)
        discussion_url = f"{self.api_endpoint}/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}"
        response = requests.delete(discussion_url, headers=self.api_headers)
        if 200 <= response.status_code < 300:
            return True
        return False


class GitlabDiscussionEngine(GitlabEngine):
    """"""


class GitlabIssueDiscussionEngine(GitlabDiscussionEngine):
    """XIA Document Engine based on Gitlab Discussion Pages
    """
    engine_param = "gitlab_issue_discussion"
    engine_connector_class = GitlabEngineParam
    engine_connector = GitlabIssueDiscussionEngineClient

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None) -> str:
        db_con = cls.get_connection(document_class)
        project_name = db_content["target"]
        issue_name = db_content["mission"]
        discussion_content = cls.db_to_content(document_class, db_content)
        created = db_con.create_discussion(project_name, issue_name, discussion_content)
        new_id = document_class.dict_to_id({
            "target": db_content["target"], "mission": db_content["mission"], "dialog_id": created["id"]
        })
        return new_id

    @classmethod
    def get(cls, document_class: Type[BaseDocument], doc_id: str) -> dict:
        db_con = cls.get_connection(document_class)
        doc_dict = document_class.id_to_dict(doc_id)
        discussion_content = db_con.get_discussion(doc_dict["target"], doc_dict["mission"], doc_dict["dialog_id"])
        if not discussion_content:
            return {}  # No data found
        doc_data = cls.content_to_dict(document_class, discussion_content)
        doc_dict.update(doc_data)
        doc_dict["_id"] = doc_id
        return doc_dict

    @classmethod
    def set(cls, document_class: Type[BaseDocument], doc_id: str, db_content: dict) -> str:
        db_con = cls.get_connection(document_class)
        doc_dict = document_class.id_to_dict(doc_id)
        discussion_content = cls.db_to_content(document_class, db_content)
        db_con.update_discussion(doc_dict["target"], doc_dict["mission"], doc_dict["dialog_id"], discussion_content)
        return doc_id

    @classmethod
    def update(cls, _document_class: Type[BaseDocument], _doc_id: str, **kwargs) -> dict:
        db_con = cls.get_connection(_document_class)
        doc_dict = _document_class.id_to_dict(_doc_id)
        discussion_content = db_con.get_discussion(doc_dict["target"], doc_dict["mission"], doc_dict["dialog_id"])
        doc_data = cls.content_to_dict(_document_class, discussion_content)
        doc_dict.update(doc_data)
        doc_dict.update(**kwargs)
        discussion_content = cls.db_to_content(_document_class, doc_dict)
        db_con.update_discussion(doc_dict["target"], doc_dict["mission"], doc_dict["dialog_id"], discussion_content)
        return cls.get(_document_class, _doc_id)

    @classmethod
    def fetch(cls, document_class: Type[BaseDocument], *args):
        db_con = cls.get_connection(document_class)
        for doc_id in args:
            doc_dict = document_class.id_to_dict(doc_id)
            discussion_content = db_con.get_discussion(doc_dict["target"], doc_dict["mission"], doc_dict["dialog_id"])
            if discussion_content:
                doc_data = cls.content_to_dict(document_class, discussion_content)
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
        db_con.delete_discussion(doc_dict["target"], doc_dict["mission"], doc_dict["dialog_id"])
