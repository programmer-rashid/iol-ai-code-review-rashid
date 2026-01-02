import json
from openai import OpenAI
from prompt import SYSTEM_PROMPT

client = OpenAI()


def review_diff(diff_text: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Review the following code diff:\n\n{diff_text}"}
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception:
        # fallback if model returns text
        return [{
            "file": "unknown",
            "line": 0,
            "severity": "SUGGESTION",
            "message": content,
            "suggested_fix": ""
        }]
