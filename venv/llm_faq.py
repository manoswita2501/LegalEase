import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def answer_faq(question: str, jurisdiction: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY is missing. Put it in your .env."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are LegalEase, an AI legal information assistant (not a lawyer).

Answer the user's legal question in a clear, beginner-friendly way.
Constraints:
- Not legal advice. Provide general educational information.
- Ask 2–4 clarifying questions if needed.
- Give practical next steps (non-legal-advice).
- Mention jurisdiction differences if relevant, but avoid claiming specific statutes.
- Output MUST be Markdown.
- End with: "Disclaimer: This is not legal advice."

Jurisdiction: {jurisdiction}

Question: {question}
""".strip()

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0.2},
    )
    return (resp.text or "").strip()
