from typing import Literal

from pydantic import BaseModel, Field

from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


# ==========================================
# Structured AI Response
# ==========================================

class FinanceAnalysis(BaseModel):

    classification: Literal[
        "UNEXPECTED_FEE",
        "AMOUNT_MISMATCH",
        "MISSING_SETTLEMENT",
        "MISSING_BANK_TRANSACTION",
        "BANK_REFERENCE_MISMATCH",
        "DELAYED_SETTLEMENT",
        "DUPLICATE_SETTLEMENT",
        "EXPECTED_FEE",
        "UNKNOWN_EXCEPTION"
    ] = Field(
        description="The most likely financial exception type."
    )

    confidence: float = Field(
        description="Confidence between 0 and 1."
    )

    reason: str = Field(
        description="Concise explanation based only on the provided evidence."
    )

    recommended_action: str = Field(
        description="Recommended next action for the finance team."
    )

    priority: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ] = Field(
        description="Priority of investigating this exception."
    )


# ==========================================
# Gemini Client
# ==========================================

if not GEMINI_API_KEY:

    client = None

else:

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# ==========================================
# Analyze Exception
# ==========================================

def analyze_exception(
    evidence: dict
):

    if client is None:

        raise ValueError(
            "GEMINI_API_KEY is not configured."
        )

    prompt = f"""
You are a financial reconciliation analyst.

Analyze the following payment reconciliation
exception.

IMPORTANT RULES:

1. Use ONLY the supplied evidence.
2. Do not invent transactions.
3. Do not invent fees.
4. Do not assume a discrepancy is valid without evidence.
5. Explain the discrepancy clearly.
6. Recommend an action for a finance operations team.
7. Return a confidence score between 0 and 1.
8. If evidence is insufficient, classify it as UNKNOWN_EXCEPTION.

FINANCIAL EVIDENCE:

{evidence}
"""

    response = client.models.generate_content(

        model=GEMINI_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=FinanceAnalysis

        )
    )

    if not response.text:

        raise ValueError(
            "Gemini returned an empty response."
        )

    result = FinanceAnalysis.model_validate_json(
        response.text
    )

    # Application-side validation
    if not 0 <= result.confidence <= 1:

        raise ValueError(
            "Gemini returned invalid confidence."
        )

    return result