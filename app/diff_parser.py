def parse_diff(diff_text: str):
    files = []
    current = None

    for line in diff_text.splitlines():
        if line.startswith("diff --git"):
            if current:
                files.append(current)
            current = {"file": None, "lines": []}

        elif line.startswith("+++ b/"):
            current["file"] = line.replace("+++ b/", "").strip()

        elif line.startswith("+") and not line.startswith("+++"):
            current["lines"].append(line[1:])

    if current:
        files.append(current)

    return files
