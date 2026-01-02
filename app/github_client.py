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

    def post_issue_comment(self, pr_number: int, body: str):
        url = f"https://api.github.com/repos/{self.repo}/issues/{pr_number}/comments"
        r = requests.post(url, headers=self._headers(), json={"body": body})
        r.raise_for_status()

    def post_inline_comment(self, pr_number, commit_sha, path, line, body):
        url = f"https://api.github.com/repos/{self.repo}/pulls/{pr_number}/comments"

        payload = {
            "body": body,
            "commit_id": commit_sha,
            "path": path,
            "line": line,
            "side": "RIGHT",
        }

        r = requests.post(url, headers=self._headers(), json=payload)

        # Inline comments may fail → fallback later
        return r
