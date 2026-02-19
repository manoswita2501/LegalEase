import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def ask_gemini(user_query: str, jurisdiction: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY is missing. Put it in your .env."

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are LegalEase, an AI legal information assistant (not a lawyer).

Rules:
- Provide general educational information only, not legal advice.
- Laws vary by jurisdiction; be cautious and state assumptions.
- Do NOT help with wrongdoing (fraud, forgery, evasion, harassment, violence).
- If the situation seems urgent/high-stakes, advise consulting a licensed attorney.
- Keep the response clear and structured.

Context:
Jurisdiction: {jurisdiction}

User question:
{user_query}

Respond in this format:
1) Plain-English explanation : (3–6 lines)
2) Practical checklist :- (5–10 bullets)
3) Red flags / common mistakes :- (3–7 bullets)
4) What info a lawyer would ask for? (max 6 bullets)
5) Disclaimer :- (one line)
""".strip()

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": 0.2},
    )
    return (resp.text or "").strip()
