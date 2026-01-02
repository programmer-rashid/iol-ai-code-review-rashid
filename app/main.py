import json
import os
from github_client import GitHubClient
from diff_parser import parse_diff
from reviewer import review_diff
from severity import format_review_comment


def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")

    if not event_path:
        print("No GitHub event payload found")
        return

    with open(event_path) as f:
        event = json.load(f)

    pull_request = event.get("pull_request")
    if not pull_request:
        print("Not a PR event")
        return

    pr_number = pull_request["number"]
    print(f"Reviewing PR #{pr_number}")

    github = GitHubClient()

    diff = github.get_diff(pr_number)
    review_items = review_diff(diff)

    comment_body = format_review_comment(review_items)

    github.post_comment(pr_number, comment_body)

    print("Review comment posted")


if __name__ == "__main__":
    main()
