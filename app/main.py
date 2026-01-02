import json
import os
from github_client import GitHubClient
from diff_parser import parse_diff


def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")

    if not event_path or not os.path.exists(event_path):
        print("❌ GITHUB_EVENT_PATH not found")
        return

    with open(event_path, "r") as f:
        event = json.load(f)

    # Extract PR number
    pull_request = event.get("pull_request")
    if not pull_request:
        print("❌ Not a pull request event")
        return

    pr_number = pull_request["number"]
    print(f"✅ Processing PR #{pr_number}")

    # Fetch diff
    github = GitHubClient()
    diff_text = github.get_diff(pr_number)

    print("\n===== RAW DIFF START =====")
    print(diff_text[:3000])  # limit output
    print("===== RAW DIFF END =====")

    # Parse diff
    files = parse_diff(diff_text)

    print("\nParsed files:")
    for f in files:
        print(f"- {f['file']} ({len(f['lines'])} changed lines)")


if __name__ == "__main__":
    main()
