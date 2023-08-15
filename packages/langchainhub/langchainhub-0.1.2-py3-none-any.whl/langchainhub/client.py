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

def parse_owner_repo_commit(identifier: str) -> tuple[str, str, Optional[str]]:
    """
    Parses a string in the format of `owner/repo:commit` and returns a tuple of
    (owner, repo, commit).
    """
    owner_repo = identifier
    commit = None
    if ":" in identifier:
        owner_repo, commit = identifier.split(":", 1)
    
    if "/" not in owner_repo:
        raise ValueError(
            f"Invalid identifier {identifier}. "
            "Identifier must be in the format of `owner/repo:commit or owner/repo`."
        )
    owner, repo = owner_repo.split("/", 1)
    return owner, repo, commit

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

    def _get_latest_commit_hash(self, repo_full_name: str) -> Optional[str]:
        commits_resp = self.list_commits(repo_full_name)
        commits = commits_resp["commits"]
        if len(commits) == 0:
            return None
        return commits[0]["commit_hash"]

    def push(self, repo_full_name: str, manifest_json: str, *, parent_commit_hash: Optional[str] = "latest"):
        manifest_dict = json.loads(manifest_json)
        if parent_commit_hash == "latest":
            parent_commit_hash = self._get_latest_commit_hash(repo_full_name)
        request_dict = {"parent_commit": parent_commit_hash, "manifest": manifest_dict}
        res = requests.post(
            f"{self.api_url}/commits/{repo_full_name}",
            headers=self._get_headers(),
            json=request_dict,
        )
        res.raise_for_status()
        return res.json()

    def pull(self, owner_repo_commit: str):
        owner, repo, commit_hash = parse_owner_repo_commit(owner_repo_commit)
        if commit_hash is None or commit_hash == "latest":
            commit_hash = self._get_latest_commit_hash(f"{owner}/{repo}")
            if commit_hash is None:
                raise ValueError("No commits found")
        res = requests.get(
            f"{self.api_url}/commits/{owner}/{repo}/{commit_hash}",
            headers=self._get_headers(),
        )
        res.raise_for_status()
        res_dict = res.json()
        return json.dumps(res_dict["manifest"])
