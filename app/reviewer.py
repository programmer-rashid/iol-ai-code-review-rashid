from openai import OpenAI
from prompt import SYSTEM_PROMPT

client = OpenAI()


def review_diff(diff_text: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Review the following code diff:\n\n{diff_text}"
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.2,
    )

    return response.choices[0].message.content
