import os
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

def _clean(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s

def review_document(text: str, jurisdiction: str, doc_type_hint: str = "") -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY is missing. Put it in your .env."

    client = genai.Client(api_key=api_key)

    text = _clean(text)
    if not text:
        return "Error: No document text found."

    prompt = f"""
You are LegalEase, an AI legal information assistant (not a lawyer).

Task: Review the document text and produce a structured analysis.
Constraints:
- Do NOT provide legal advice; provide general informational analysis.
- Do NOT invent text not present. If something is missing/unclear, say so.
- Limit the summary to 5-6 bullets max.
- If the document is too long, focus on the most important parts and say it's truncated.
- Output MUST be Markdown only.
- Keep it concise but useful.

Context:
Jurisdiction: {jurisdiction}
Document type hint (may be empty): {doc_type_hint}

Return in EXACT sections with these headings:

## Summary
- ...

## Key Clauses / Terms
- Parties:
- Dates:
- Payment:
- Term & termination:
- Confidentiality:
- IP / ownership:
- Liability / indemnity:
- Dispute resolution / governing law:
(If not found, write "Not found / unclear".)

## Risks / Red Flags
- ...

## Suggested Improvements / Questions to Ask
- ...

End with: "Disclaimer: This is not legal advice."

DOCUMENT TEXT:
---
{text}
---
""".strip()

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0.2},
    )
    return (resp.text or "").strip()
