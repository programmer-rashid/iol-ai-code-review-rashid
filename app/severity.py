def format_review_comment(items):
    """
    Convert AI JSON output into a readable PR comment.
    """
    if not items:
        return "✅ No major issues found."

    blocks = []

    for item in items:
        severity = item.get("severity", "SUGGESTION").upper()
        file = item.get("file", "unknown")
        line = item.get("line", 0)
        message = item.get("message", "")
        fix = item.get("suggested_fix", "")

        # Fixed: Added closing ``` backticks for the markdown block
        block = f"""
### {severity}
**File:** `{file}`  
**Line:** {line}

{message}

💡 **Suggested fix:**
```text
{fix}
""" blocks.append(block.strip())
return "\n\n".join(blocks)