import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

DOC_TYPES = [
    "Mutual NDA",
    "One-way NDA",
    "Service Agreement / Freelance Contract",
    "Employment Offer Letter",
    "Consulting Agreement",
    "Partnership Agreement",
    "Rental Agreement / Addendum",
    "Demand / Notice Letter",
    "MoU (Memorandum of Understanding)",
    "Invoice / Payment Terms Addendum",
    "Other (custom)"
]

def recommend_doc(user_query: str, jurisdiction: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY is missing. Put it in your .env."}

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are LegalEase, an AI legal information assistant (not a lawyer).

Task:
Recommend the most suitable legal document type based on the user's query.
Be conservative and jurisdiction-aware. If uncertain, ask clarifying questions.

Jurisdiction: {jurisdiction}
User query: {user_query}

Return STRICT JSON only (no extra text) with this schema:
{{
  "recommended_document": "<one of: {DOC_TYPES}>",
  "alternatives": ["<up to 3 from list>"],
  "why_this_document": ["<3-6 bullets as strings>"],
  "required_information": ["<fields user must provide>"],
  "follow_up_questions": ["<up to 5 questions if needed>"],
  "risk_notes": ["<up to 5 red-flag notes>"]
}}

Rules:
- The recommended_document must be exactly one of the allowed doc types.
- If user asks for something illegal or suspicious, set recommended_document to "Other (custom)" and include a refusal-style risk note.
""".strip()

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0.2},
    )

    raw = (resp.text or "").strip()

    # Defensive JSON extraction
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return {"error": "Model did not return JSON.", "raw": raw}

    try:
        data = json.loads(raw[start:end+1])
    except json.JSONDecodeError:
        return {"error": "Invalid JSON returned.", "raw": raw}

    return data
