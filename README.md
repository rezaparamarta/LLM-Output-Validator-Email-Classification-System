📌 Project Overview

This project demonstrates how to:

Generate structured output from an LLM

Enforce strict schema validation using Pydantic

Handle malformed or invalid AI responses

Build a clean and production-ready validation workflow

The system classifies emails into structured categories such as:

Category (work, urgent, spam, etc.)

Priority level

Sentiment

Action requirements

Extracted action items

🏗️ Architecture
```
User Email Input
        ↓
OpenAI LLM (Structured Output)
        ↓
Pydantic Validation Layer
        ↓
Validated JSON Output
        ↓
Error Handling (if invalid)
```

🛠️ Tech Stack
```
Python 3.10+
OpenAI API (gpt-4.1-mini)
Pydantic v2
Virtual Environment (venv)
```

📂 Project Structure
```
llm-output-validator/
│
├── email_classifier_validator.py
├── requirements.txt
├── .env
└── README.md

```

⚙️ Setup & Installation
1️⃣ Clone Repository
```
git clone https://github.com/yourusername/llm-output-validator.git
cd llm-output-validator
```

2️⃣ Create Virtual Environment
```
python -m venv venv
```

Activate Virtual Environment
```
venv\Scripts\activate
```

3️⃣ Install Dependencies
```
pip install openai pydantic python-dotenv
```

4️⃣ Set Environment Variable
Create a .env file:

```
OPENAI_API_KEY=your_api_key_here
```

5️⃣ Run the Project

```
python email_classifier_validator.py
```
🧠 Pydantic Validation Model

The LLM response must conform to this schema:
```
class EmailClassifierOutput(BaseModel):
    category: Literal["work", "urgent", "personal", "spam", "social"]
    priority: Literal["low", "medium", "high", "critical"]
    summary: str = Field(..., min_length=10, max_length=200)
    requires_action: bool
    sentiment: Literal["positive", "neutral", "negative"]
    action_items: List[str] = Field(default_factory=list)
    deadline: Optional[str] = None
    sender_type: Optional[Literal["colleague", "client", "friend", "automated"]] = None
```

This ensures:

No hallucinated categories

No invalid priorities

Proper summary length

Correct boolean and structured fields

```
{
  "category": "urgent",
  "priority": "critical",
  "summary": "Server downtime detected requiring immediate action.",
  "requires_action": true,
  "sentiment": "negative",
  "action_items": ["Investigate server logs", "Restart service"],
  "deadline": null,
  "sender_type": "automated"
}

```

🛡️ Why Validation Matters

LLMs can:

Return invalid categories

Generate malformed JSON

Produce values outside constraints

This project ensures:

✔️ Structured output
✔️ Strict schema enforcement
✔️ Clear validation errors
✔️ Production-safe AI integration

🚀 Future Improvements

Add retry mechanism on validation failure

Integrate FastAPI endpoint

Add logging & monitoring

Add unit tests with pytest

Extend to multilingual email classification

```
👨‍💻 Author

Reza Paramarta
Software Test Engineer | QA Automation | AI/NLP Enthusiast
```
