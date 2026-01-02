import os
import requests


class GitHubClient:
    def __init__(self):
        self.repo = os.environ.get("GITHUB_REPOSITORY")
        self.token = os.environ.get("GITHUB_TOKEN")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3.diff"
        }

    def get_diff(self, pr_number: int) -> str:
        url = f"https://api.github.com/repos/{self.repo}/pulls/{pr_number}"
        response = requests.get(url, headers=self._headers())

        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch diff: {response.status_code} {response.text}"
            )

        return response.text
