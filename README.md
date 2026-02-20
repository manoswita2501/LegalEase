# LegalEase ⚖️

LegalEase is an AI-driven legal assistant built with Streamlit and powered by the Gemini API. It is designed to simplify routine legal workflows by helping users quickly understand legal concepts, choose the right legal document, draft structured agreements, and review contracts efficiently. This web application focuses on improving access to legal documentation for individuals who may have limited access to legal resources. By guiding users through document drafting and highlighting key risks during review, it aims to save time, reduce avoidable errors, and make legal information easier to navigate for everyone.

## Key Features

* **AI Legal Chat:** Ask legal questions in plain language and receive structured, jurisdiction-aware informational responses.
* **Document Recommendation:** Describe a situation and receive a recommended document type, along with required details and practical follow-up questions.
* **Legal Document Drafting:** Generate clean drafts for common documents using interactive forms, with an optional AI polish step to improve clarity.
* **Document Review and Summarization:** Upload or paste contract text (including PDF upload) to get a summary, key clauses, and red-flag risks.
* **FAQ and Knowledge Base:** A curated set of common legal questions with AI-generated explanations, plus support for custom questions.
* **Legal Resources:** A curated repository of official and reliable portals and references to help users find the right starting point quickly.

## Tech Stack

* **Frontend/UI:** Streamlit
* **LLM:** Google Gemini API (via 'google-genai')
* **PDF extraction:** PyMuPDF ('pymupdf')
* **Environment management:** Python 'venv', '.env' for secrets (like API key)

## Known Limitations

* LegalEase is **informational**, not a substitute for professional legal advice.
* PDF extraction works best on **digital PDFs**. Scanned image-only PDFs may not extract text unless OCR is added.
* Generated drafts are templates and should be reviewed properly.

## Future Improvements I hope to incorporate

* OCR support for scanned PDFs
* User accounts + saved drafts/reviews
* Clause library and clause insertion into drafts
* Export bundle as ZIP file for generated artifacts
* More document templates and jurisdiction-specific variations (for different Indian states)


