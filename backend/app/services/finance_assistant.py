from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


if GEMINI_API_KEY:

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

else:

    client = None


def ask_finance_assistant(
    question: str,
    context: dict
):

    if client is None:

        raise ValueError(
            "GEMINI_API_KEY is not configured."
        )

    prompt = f"""
You are LedgerPilot AI,
a finance operations assistant.

Answer the user's question using ONLY
the reconciliation data provided below.

Do not invent financial data.

If the information is insufficient,
say that clearly.

RECONCILIATION DATA:

{context}

USER QUESTION:

{question}

Give a concise, professional finance-operations answer.
"""

    response = client.models.generate_content(

        model=GEMINI_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(
            temperature=0.2
        )
    )

    return response.text