import streamlit as st
from common import sidebar

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

jurisdiction, ack = sidebar()

st.markdown(
    """
<div style="padding: 8px 0 4px 0;">
  <div style="font-size:2.2rem; font-weight:900; color:#0f172a; line-height:1.1;">
    LegalEase
  </div>
  <div style="margin-top:6px; font-size:1.05rem; color: rgba(2,6,23,0.70);">
    AI-driven legal support for document drafting, document review, and legal information — fast, structured, and usable.
  </div>
</div>
""",
    unsafe_allow_html=True
)

st.write("")

c1, c2, c3 = st.columns([1.1, 1, 0.9])
with c1:
    st.markdown(
        f"""
<div style="background:#ffffff; border:1px solid rgba(2,6,23,0.08); border-radius:18px; padding:16px 18px;
            box-shadow:0 1px 2px rgba(2,6,23,0.05);">
  <div style="color: rgba(2,6,23,0.65); font-size:0.95rem;">Selected jurisdiction</div>
  <div style="color:#2563eb; font-size:1.35rem; font-weight:900; margin-top:2px;">{jurisdiction}</div>
  <div style="margin-top:10px; color: rgba(2,6,23,0.72); line-height:1.4;">
    LegalEase adapts prompts and output for the selected jurisdiction where possible.
  </div>
</div>
""",
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
<div style="background:#ffffff; border:1px solid rgba(2,6,23,0.08); border-radius:18px; padding:16px 18px;
            box-shadow:0 1px 2px rgba(2,6,23,0.05);">
  <div style="color: rgba(2,6,23,0.65); font-size:0.95rem;">What you can do</div>
  <ul style="margin-top:8px; color: rgba(2,6,23,0.75); line-height:1.55;">
    <li>Ask legal questions (chat)</li>
    <li>Get document recommendations</li>
    <li>Generate drafts (NDA, service agreement, offer letter, notice)</li>
    <li>Review PDFs and contracts</li>
    <li>Use curated legal resources</li>
  </ul>
</div>
""",
        unsafe_allow_html=True
    )

with c3:
    status = "Enabled" if ack else "Disabled"
    color = "#16a34a" if ack else "#ef4444"
    st.markdown(
        f"""
<div style="background:#ffffff; border:1px solid rgba(2,6,23,0.08); border-radius:18px; padding:16px 18px;
            box-shadow:0 1px 2px rgba(2,6,23,0.05);">
  <div style="color: rgba(2,6,23,0.65); font-size:0.95rem;">Disclaimer acknowledgement</div>
  <div style="color:{color}; font-size:1.35rem; font-weight:900; margin-top:2px;">{status}</div>
  <div style="margin-top:10px; color: rgba(2,6,23,0.72); line-height:1.4;">
    Turn it on in the sidebar to unlock drafting and review features.
  </div>
</div>
""",
        unsafe_allow_html=True
    )

st.write("")
st.markdown("## Quick Start")

st.markdown(
    """
<div style="background:#ffffff; border:1px solid rgba(2,6,23,0.08); border-radius:18px; padding:14px 16px;
            box-shadow:0 1px 2px rgba(2,6,23,0.05);">
  <div style="color: rgba(2,6,23,0.72); line-height:1.55;">
    <b>Suggested flow:</b>
    <span style="color:#2563eb; font-weight:800;">Recommend</span> → 
    <span style="color:#2563eb; font-weight:800;">Draft</span> → 
    <span style="color:#2563eb; font-weight:800;">Review</span> → 
    <span style="color:#2563eb; font-weight:800;">FAQ</span> → 
    <span style="color:#2563eb; font-weight:800;">Resources</span>
  </div>
</div>
""",
    unsafe_allow_html=True
)

st.write("")

st.markdown("## Features")

f1, f2, f3 = st.columns(3)
with f1:
    st.page_link("pages/chat.py", label="Chat", icon="💬")
    st.caption("Ask legal questions and get structured, jurisdiction-aware informational responses.")
with f2:
    st.page_link("pages/recommend.py", label="Document Recommendation", icon="🧭")
    st.caption("Describe your situation → LegalEase suggests the most relevant document to generate.")
with f3:
    st.page_link("pages/draft.py", label="Draft Generator", icon="📝")
    st.caption("Interactive forms + templates + optional AI polish, with download as Markdown.")

f4, f5, f6 = st.columns(3)
with f4:
    st.page_link("pages/review.py", label="Review & Summarize", icon="🔎")
    st.caption("Upload .txt/.pdf or paste text → get summary, key clauses, risks, and questions.")
with f5:
    st.page_link("pages/faq.py", label="FAQ & Knowledge Base", icon="📚")
    st.caption("Click common questions or ask your own. Download answers as Markdown.")
with f6:
    st.page_link("pages/resources.py", label="Legal Resources", icon="🌐")
    st.caption("Curated portals and references, searchable and tag-filtered by jurisdiction.")

st.markdown("---")
st.markdown(
    """
<div style="color: rgba(2,6,23,0.65); font-size:0.95rem; line-height:1.5;">
<b>Important:</b> LegalEase is an informational assistant and drafting helper. It does not provide legal advice,
and it does not create an attorney-client relationship. For urgent or high-stakes matters, consult a licensed attorney.
</div>
""",
    unsafe_allow_html=True
)
