# AI Code Review Assistant

An AI-powered GitHub Pull Request reviewer that automatically analyzes code changes and posts structured, actionable feedback directly on pull requests.

The system uses a Large Language Model (LLM) to detect:
- Code quality issues
- Potential bugs and anti-patterns
- Security risks
- Performance concerns
- Best-practice violations

It is designed to be configurable, extensible, and easy to integrate into existing CI pipelines.

## Why this project?

Manual code reviews are time-consuming and inconsistent. Reviewers often miss:
- Security vulnerabilities
- Performance regressions
- Repeated bad patterns
- Missing best practices

This project automates the **first-pass review**, allowing engineers to:
- Catch common issues early
- Maintain consistent standards
- Reduce review time
- Focus on higher-level design feedback

## Architecture Overview

GitHub Pull Request
|
GitHub Actions (CI Trigger)
|
Python Review Service
├── Diff Parser
├── Config Loader
├── LLM Reviewer
├── Severity Filter
|
GitHub PR Comment API


The workflow is event-driven and executes automatically whenever a pull request is opened or updated.

## How It Works

1. A pull request is created or updated.
2. GitHub Actions triggers the workflow.
3. The workflow:
   - Loads the pull request metadata
   - Fetches the code diff from GitHub
   - Parses changed files and lines
4. The diff is sent to an LLM with a structured prompt.
5. The LLM returns structured feedback with:
   - Severity level
   - File name
   - Line reference
   - Explanation
   - Suggested fix
6. Results are filtered using `.ai-review.yaml`.
7. A formatted review comment is posted back to the PR.

## Prerequisites

- Python 3.9+
- Git
- GitHub account
- GitHub repository with Actions enabled
- OpenAI API key (or compatible LLM provider)

## Setup Instructions

### 1. Clone the repository

git clone https://github.com/programmer-rashid/iol-ai-code-review-rashid.git
cd iol-ai-code-review-rashid

2. Install dependencies
pip install -r requirements.txt

3. Configure secrets

Add the following GitHub repository secret:

OPENAI_API_KEY

GitHub → Settings → Secrets and variables → Actions → New repository secret

4. Create configuration file

Create .ai-review.yaml in the repository root:

ignore:
  - tests/
  - docs/

severity_threshold: warning
max_comments: 10




## Example Output

When a pull request is opened, the bot posts a comment like:

### WARNING
File: app/main.py  


Possible unsafe string interpolation detected.

 Suggested fix:

Use parameterized queries instead of string formatting.




## Limitations

- Analysis is heuristic and LLM-based, not a full static analyzer
- Line numbers are approximate
- Large diffs may be truncated
- Language-specific rules are limited
- Inline (line-level) review comments are not yet implemented

## Future Improvements

- Inline GitHub review comments
- Multi-language support
- AST-based parsing
- Token-aware chunking
- Caching & deduplication
- Model selection via config
- Confidence scoring
- SARIF export
