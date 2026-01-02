import os
import requests


class GitHubClient:
    def __init__(self):
        self.repo = os.environ.get("GITHUB_REPOSITORY")
        self.token = os.environ.get("GITHUB_TOKEN")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def get_diff(self, pr_number: int) -> str:
        url = f"https://api.github.com/repos/{self.repo}/pulls/{pr_number}"
        headers = self._headers()
        headers["Accept"] = "application/vnd.github.v3.diff"

        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.text

    def post_comment(self, pr_number: int, body: str):
        url = f"https://api.github.com/repos/{self.repo}/issues/{pr_number}/comments"
        resp = requests.post(url, headers=self._headers(), json={"body": body})
        resp.raise_for_status()
