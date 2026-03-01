from typing import Optional, Literal, List
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


# ==============================
# Step 1 — Pydantic Model
# ==============================

class EmailClassifierOutput(BaseModel):
    category: Literal["work", "urgent", "personal", "spam", "social"]
    priority: Literal["low", "medium", "high", "critical"]
    summary: str = Field(..., min_length=10, max_length=200)
    requires_action: bool
    sentiment: Literal["positive", "neutral", "negative"]

    action_items: List[str] = Field(default_factory=list)
    deadline: Optional[str] = None
    sender_type: Optional[
        Literal["colleague", "client", "friend", "automated"]
    ] = None


# ==============================
# Step 2 — OpenAI Client
# ==============================

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # API key must be set in environment variable


# ==============================
# Step 3 — LLM Call Function
# ==============================

def classify_email(email_text: str) -> EmailClassifierOutput:
    completion = client.beta.chat.completions.parse(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an email classification assistant. Classify emails accurately with category, priority, and sentiment."
            },
            {
                "role": "user",
                "content": email_text
            }
        ],
        response_format=EmailClassifierOutput
    )

    return completion.choices[0].message.parsed


# ==============================
# Step 4 — Validation Handler
# ==============================

def validate_and_print(response):
    try:
        validated = EmailClassifierOutput(**response.model_dump())
        print("✅ Valid classification:")
        print(validated.model_dump_json(indent=2))
    except ValidationError as e:
        print("❌ Validation error:")
        for error in e.errors():
            field = ".".join(map(str, error["loc"]))
            print(f"Field: {field} | Error: {error['msg']}")


# ==============================
# Step 5 — Run Examples
# ==============================

if __name__ == "__main__":

    emails = [
        "Dear team, the quarterly budget meeting is rescheduled to Friday at 3 PM. Please confirm attendance.",
        "URGENT: Server downtime detected. System critical. Immediate action required.",
        "Hi! Just wanted to check in and see how your weekend was. Let's grab coffee soon!"
    ]

    for email in emails:
        print("\n--- Processing Email ---")
        llm_response = classify_email(email)
        validate_and_print(llm_response)