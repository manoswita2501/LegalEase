import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def polish_markdown(draft_md: str, jurisdiction: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY is missing. Put it in your .env."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are LegalEase, an AI legal information assistant (not a lawyer).

Task:
Polish the following legal document draft for clarity, consistency, and professional tone.
Important constraints:
- DO NOT add new legal obligations or remove obligations.
- DO NOT change parties, term, purpose, governing law, or meaning.
- Preserve headings/sections and signature blocks.
- Output MUST be valid Markdown.
- Keep it conservative and readable.
- Add a single-line disclaimer at the end: "Disclaimer: This is not legal advice."

Jurisdiction context: {jurisdiction}

DRAFT (Markdown):
---
{draft_md}
---
Return ONLY the polished Markdown, nothing else.
""".strip()

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0.2},
    )
    return (resp.text or "").strip()


def draft_custom_markdown(spec: dict, jurisdiction: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY is missing. Put it in your .env."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are LegalEase, an AI legal information assistant (not a lawyer).

Generate a clean, professional legal-style draft in Markdown based strictly on the user's inputs.
Hard constraints:
- This is informational drafting help, not legal advice.
- Do NOT invent facts that are not provided.
- If a detail is missing, insert a placeholder like [ADD ...].
- Keep it conservative and generally applicable; avoid jurisdiction-specific claims unless the user provided them.
- If the user's request is for wrongdoing or evading law, refuse with a short message.
- Output MUST be Markdown only.
- End with: "Disclaimer: This is not legal advice."

Context:
Jurisdiction: {jurisdiction}

USER SPEC:
Title: {spec.get("title","")}
Doc type / category: {spec.get("doc_kind","")}
Parties: {spec.get("parties","")}
Goal: {spec.get("goal","")}
Key facts: {spec.get("facts","")}
Key terms: {spec.get("terms","")}
Clauses to include: {spec.get("clauses","")}
Tone: {spec.get("tone","")}
Signature blocks needed: {spec.get("signatures","")}
Extra instructions: {spec.get("extra","")}

Draft a document with:
- Title
- Effective date
- Parties
- Background / Purpose
- Definitions (only if needed)
- Core obligations
- Payment (if relevant)
- Term & termination
- Confidentiality (if relevant)
- IP/ownership (if relevant)
- Liability/indemnity (if relevant)
- Dispute resolution / governing law (as placeholder if not provided)
- Signatures (if requested)
""".strip()

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0.2},
    )
    return (resp.text or "").strip()
