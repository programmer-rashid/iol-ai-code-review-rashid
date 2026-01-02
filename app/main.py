import json
import os
from github_client import GitHubClient
from diff_parser import parse_diff
from reviewer import review_diff


def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")

    if not event_path:
        print("No GitHub event payload found")
        return

    with open(event_path, "r") as f:
        event = json.load(f)

    pull_request = event.get("pull_request")
    if not pull_request:
        print("Not a PR event")
        return

    pr_number = pull_request["number"]
    print(f"🔍 Reviewing PR #{pr_number}")

    github = GitHubClient()
    diff = github.get_diff(pr_number)

    print("Fetched diff")

    review_output = review_diff(diff)

    print("\n===== AI REVIEW OUTPUT =====")
    print(review_output)
    print("===== END REVIEW =====")


if __name__ == "__main__":
    main()
