from typing import Type
from functools import lru_cache
import urllib.parse
import requests
from xia_engine import BaseDocument
from xia_engine import Engine
from xia_gpt_engine_gitlab.engine import GitlabEngineParam, GitlabEngineClient, GitlabEngine
from xia_gpt_engine_gitlab.engine_issue import GitlabIssueEngineClient


class GitlabDiscussionNoteEngineClient(GitlabEngineClient):
    def create_note(self, project_name: str, parent_name: str, discussion_id: str, note_content: str):
        """Create note page

        Args:
            project_name: Project name
            parent_name: Parent name which could hold the note
            discussion_id: Discussion ID
            note_content: database content
        """

    def get_note(self, project_name: str, parent_name: str, discussion_id: str, note_id: int):
        """Update note page

        Args:
            project_name: Project name
            parent_name: Parent name which could hold the note
            discussion_id: Discussion ID
            note_id: Note ID
        """

    def update_note(self, project_name: str, parent_name: str, discussion_id: str, note_id: int, note_content: str):
        """Update Note

        Args:
            project_name: Project name
            parent_name: Parent name which could hold the note
            discussion_id: Discussion ID
            note_id: Note ID
            note_content: Note content
        """

class GitlabIssueDiscussionNoteEngineClient(GitlabDiscussionNoteEngineClient):
    def create_note(self, project_name: str, parent_name: str, discussion_id: str, note_content: str):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_iid = GitlabIssueEngineClient.get_issue_iid_from_name(self.api_endpoint, self.api_token, project_id,
                                                                    parent_name)
        note_url = f"{self.api_endpoint}/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}/notes"
        payload = {"body": note_content}
        response = requests.post(note_url, headers=self.api_headers, data=payload)
        self.check_response(response)
        return response.json()

    def update_note(self, project_name: str, parent_name: str, discussion_id: str, note_id: int, note_content: str):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_iid = GitlabIssueEngineClient.get_issue_iid_from_name(self.api_endpoint, self.api_token, project_id,
                                                                    parent_name)
        note_url = f"{self.api_endpoint}/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}/" \
                   f"notes/{note_id}"
        payload = {"body": note_content}
        response = requests.put(note_url, headers=self.api_headers, data=payload)
        self.check_response(response)

    def get_note(self, project_name: str, parent_name: str, discussion_id: str, note_id: int):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_iid = GitlabIssueEngineClient.get_issue_iid_from_name(self.api_endpoint, self.api_token, project_id,
                                                                    parent_name)
        note_url = f"{self.api_endpoint}/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}/" \
                   f"notes/{note_id}"
        response = requests.get(note_url, headers=self.api_headers)
        if response.status_code == 200:
            return response.json()["body"]
        return ""

    def delete_note(self, project_name: str, parent_name: str, discussion_id: str, note_id: int):
        project_id = self.get_project_id_from_name(self.api_endpoint, self.api_token, project_name)
        issue_iid = GitlabIssueEngineClient.get_issue_iid_from_name(self.api_endpoint, self.api_token, project_id,
                                                                    parent_name)
        note_url = f"{self.api_endpoint}/projects/{project_id}/issues/{issue_iid}/discussions/{discussion_id}/" \
                   f"notes/{note_id}"
        response = requests.delete(note_url, headers=self.api_headers)
        if 200 <= response.status_code < 300:
            return True
        return False


class GitlabDiscussionNoteEngine(GitlabEngine):
    """"""


class GitlabIssueDiscussionNoteEngine(GitlabDiscussionNoteEngine):
    """XIA Document Engine based on Gitlab Note Pages with Issue and Discussion as parent
    """
    engine_param = "gitlab_issue_discussion_note"
    engine_connector_class = GitlabEngineParam
    engine_connector = GitlabIssueDiscussionNoteEngineClient

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None) -> str:
        db_con = cls.get_connection(document_class)
        project_name = db_content["target"]
        issue_name = db_content["mission"]
        discussion_id = db_content["dialog_id"]
        note_content = db_content["body"]
        created = db_con.create_note(project_name, issue_name, discussion_id, note_content)
        new_id = document_class.dict_to_id({
            "target": db_content["target"],
            "mission": db_content["mission"],
            "dialog_id": db_content["dialog_id"],
            "turn_id": created["id"]
        })
        return new_id

    @classmethod
    def get(cls, document_class: Type[BaseDocument], doc_id: str) -> dict:
        db_con = cls.get_connection(document_class)
        doc_dict = document_class.id_to_dict(doc_id)
        doc_dict["body"] = db_con.get_note(doc_dict["target"], doc_dict["mission"], doc_dict["dialog_id"],
                                           doc_dict["turn_id"])
        doc_dict["_id"] = doc_id
        return doc_dict if doc_dict["body"] else {}

    @classmethod
    def set(cls, document_class: Type[BaseDocument], doc_id: str, db_content: dict) -> str:
        db_con = cls.get_connection(document_class)
        doc_dict = document_class.id_to_dict(doc_id)
        db_con.update_note(doc_dict["target"], doc_dict["mission"], doc_dict["dialog_id"],
                           doc_dict["turn_id"], doc_dict["body"])
        return doc_id

    @classmethod
    def update(cls, _document_class: Type[BaseDocument], _doc_id: str, **kwargs) -> dict:
        db_con = cls.get_connection(_document_class)
        doc_dict = _document_class.id_to_dict(_doc_id)
        db_con.update_note(doc_dict["target"], doc_dict["mission"], doc_dict["dialog_id"],
                           doc_dict["turn_id"], kwargs["body"])
        return cls.get(_document_class, _doc_id)

    @classmethod
    def fetch(cls, document_class: Type[BaseDocument], *args):
        db_con = cls.get_connection(document_class)
        for doc_id in args:
            doc_dict = document_class.id_to_dict(doc_id)
            doc_dict["body"] = db_con.get_note(doc_dict["target"], doc_dict["mission"],
                                               doc_dict["dialog_id"], doc_dict["turn_id"])
            doc_dict["_id"] = doc_id
            if doc_dict["body"]:
                yield doc_id, doc_dict

    @classmethod
    def delete(cls, document_class: Type[BaseDocument], doc_id: str):
        db_con = cls.get_connection(document_class)
        old_data = cls.get(document_class, doc_id)
        if not old_data:
            return
        doc_dict = document_class.id_to_dict(doc_id)
        db_con.delete_note(doc_dict["target"], doc_dict["mission"], doc_dict["dialog_id"], doc_dict["turn_id"])
