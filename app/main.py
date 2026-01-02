from config import load_config
from severity import format_review_comment, filter_by_severity
from github_client import GitHubClient
from reviewer import review_diff
import json
import os


def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        return

    with open(event_path) as f:
        event = json.load(f)

    pr = event.get("pull_request")
    if not pr:
        return

    pr_number = pr["number"]
    commit_sha = pr["head"]["sha"]

    github = GitHubClient()
    config = load_config()

    diff = github.get_diff(pr_number)
    review_items = review_diff(diff)

    review_items = filter_by_severity(
        review_items,
        config.get("severity_threshold")
    )

    max_comments = config.get("max_comments", 10)
    review_items = review_items[:max_comments]

    fallback_comments = []

    for item in review_items:
        file = item.get("file")
        line = item.get("line", 1)

        comment_body = format_review_comment([item])

        # Try inline comment
        response = github.post_inline_comment(
            pr_number=pr_number,
            commit_sha=commit_sha,
            path=file,
            line=max(1, int(line)),
            body=comment_body,
        )

        # If GitHub rejects inline → fallback
        if response.status_code >= 300:
            fallback_comments.append(comment_body)

    # Fallback to summary comment
    if fallback_comments:
        github.post_issue_comment(
            pr_number,
            "\n\n".join(fallback_comments)
        )


if __name__ == "__main__":
    main()
