import json
import os
from typing import Optional

import requests


def _get_api_key(api_key: Optional[str]) -> Optional[str]:
    api_key = api_key if api_key is not None else os.getenv("LANGCHAIN_API_KEY")
    if api_key is None or not api_key.strip():
        return None
    return api_key.strip().strip('"').strip("'")


def _get_api_url(api_url: Optional[str]) -> str:
    _api_url = (
        api_url
        if api_url is not None
        else os.getenv(
            "LANGCHAINHUB_ENDPOINT",
            "http://localhost:8000",
        )
    )
    if not _api_url.strip():
        raise ValueError("LangChain Hub API URL cannot be empty")
    return _api_url.strip().strip('"').strip("'").rstrip("/")


class Client:
    """
    An API Client for LangChainHub
    """

    def __init__(self, api_url: Optional[str] = None, *, api_key: Optional[str] = None):
        self.api_url = _get_api_url(api_url)
        self.api_key = _get_api_key(api_key)

    def _get_headers(self):
        headers = {}
        if self.api_key is not None:
            headers["x-api-key"] = self.api_key
        return headers

    def set_tenant_handle(self, tenant_handle: str):
        res = requests.post(
            f"{self.api_url}/settings/handle",
            headers=self._get_headers(),
            json={"tenant_handle": tenant_handle},
        )
        res.raise_for_status()
        return res.json()

    def list_repos(self, limit: int = 100, offset: int = 0):
        res = requests.get(
            f"{self.api_url}/repos?limit={limit}&offset={offset}",
            headers=self._get_headers(),
        )
        res.raise_for_status()
        return res.json()

    def get_repo(self, repo_full_name: str):
        res = requests.get(
            f"{self.api_url}/repos/{repo_full_name}",
            headers=self._get_headers(),
        )
        res.raise_for_status()
        return res.json()

    def create_repo(
        self, repo_handle: str, *, description: str = "", is_public: bool = True
    ):
        json = {
            "repo_handle": repo_handle,
            "is_public": is_public,
            "description": description,
        }
        res = requests.post(
            f"{self.api_url}/repos/",
            headers=self._get_headers(),
            json=json,
        )
        res.raise_for_status()
        return res.json()

    def list_commits(self, repo_full_name: str, limit: int = 100, offset: int = 0):
        res = requests.get(
            f"{self.api_url}/commits/{repo_full_name}/?limit={limit}&offset={offset}",
            headers=self._get_headers(),
        )
        res.raise_for_status()
        return res.json()

    def like_repo(self, repo_full_name: str):
        res = requests.post(
            f"{self.api_url}/likes/{repo_full_name}",
            headers=self._get_headers(),
            json={"like": True},
        )
        res.raise_for_status()
        return res.json()

    def unlike_repo(self, repo_full_name: str):
        res = requests.post(
            f"{self.api_url}/likes/{repo_full_name}",
            headers=self._get_headers(),
            json={"like": False},
        )
        res.raise_for_status()
        return res.json()

    def push(self, repo_full_name: str, parent_commit_hash: str, manifest_json: str):
        manifest_dict = json.loads(manifest_json)
        request_dict = {"parent_commit": parent_commit_hash, "manifest": manifest_dict}
        res = requests.post(
            f"{self.api_url}/commits/{repo_full_name}",
            headers=self._get_headers(),
            json=request_dict,
        )
        res.raise_for_status()
        return res.json()

    def pull(self, repo_full_name: str, commit_hash: str):
        if commit_hash == "latest":
            commits_resp = self.list_commits(repo_full_name)
            commits = commits_resp["commits"]
            if len(commits) == 0:
                raise ValueError("No commits found")
            commit_hash = commits[0]["commit_hash"]
        res = requests.get(
            f"{self.api_url}/commits/{repo_full_name}/{commit_hash}",
            headers=self._get_headers(),
        )
        res.raise_for_status()
        res_dict = res.json()
        return json.dumps(res_dict["manifest"])
