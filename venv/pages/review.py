import streamlit as st
import re
from common import sidebar, apply_base_style
from llm_review import review_document
from pdf_utils import extract_pdf_text

apply_base_style()

def risk_meter(review_md: str):
    s = (review_md or "").lower()

    high = [
        "unilateral", "sole discretion", "perpetual", "irrevocable", "indemnify",
        "liquidated damages", "no refund", "non-refundable", "automatic renewal",
        "waive", "waiver", "penalty", "injunctive", "consequential damages excluded"
    ]
    med = [
        "arbitration", "governing law", "termination for convenience", "assignment",
        "confidentiality", "ip ownership", "limitation of liability", "late fee"
    ]

    score = 0
    hits = []

    for w in high:
        if w in s:
            score += 3
            hits.append(w)

    for w in med:
        if w in s:
            score += 1
            hits.append(w)

    if score >= 10:
        level = "High"
    elif score >= 5:
        level = "Medium"
    else:
        level = "Low"

    hits = sorted(set(hits))[:10]
    return level, score, hits


jurisdiction, ack = sidebar()

st.title("Review & Summarize")
st.caption("Paste or upload a document to get a structured review (informational only).")

if not ack:
    st.warning("Please acknowledge the disclaimer in the sidebar to use this feature.")
    st.stop()

st.markdown(
    f"<span style='color: rgba(2, 6, 23, 0.65);'>Jurisdiction:</span> "
    f"<span style='color:#2563eb; font-weight:600;'>{jurisdiction}</span>",
    unsafe_allow_html=True
)

st.write("")

doc_type_hint = st.selectbox(
    "Document type (optional)",
    ["", "NDA", "Service Agreement", "Employment Offer Letter", "Lease", "Terms of Service", "Other"],
    index=0
)

tab1, tab2 = st.tabs(["Paste text", "Upload file"])

text = ""

with tab1:
    text = st.text_area(
        "Paste document text",
        placeholder="Paste the contract/agreement text here…",
        height=260
    )

with tab2:
    f = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])
    if f is not None:
        try:
            raw = f.read()

            if f.name.lower().endswith(".txt"):
                text = raw.decode("utf-8", errors="ignore")
                st.success("Text file loaded.")
            else:
                text = extract_pdf_text(raw, max_pages=30)
                if text:
                    st.success("PDF loaded and text extracted.")
                else:
                    st.warning(
                        "PDF loaded, but no extractable text was found (may be scanned). "
                        "Try copy-pasting text instead."
                    )

            if text.strip():
                with st.expander("Preview extracted text"):
                    st.text_area("Extracted text", value=text[:12000], height=260)

        except Exception as e:
            st.error(f"Could not read file: {e}")

c1, c2 = st.columns([1, 1])
with c1:
    run_btn = st.button("Review document", type="primary")
with c2:
    clear_btn = st.button("Clear")

if clear_btn:
    st.session_state.pop("review_md", None)
    st.rerun()

if run_btn:
    if not text.strip():
        st.warning("Paste text or upload a .txt file first.")
        st.stop()

    with st.spinner("Reviewing…"):
        md = review_document(text.strip(), jurisdiction, doc_type_hint)

    st.session_state["review_md"] = md

md = st.session_state.get("review_md", "")
if md:
    st.write("")
    st.subheader("Review result")
    st.markdown(md)
    
    lvl, score, hits = risk_meter(md)
    
    color = {"Low": "#16a34a", "Medium": "#f59e0b", "High": "#ef4444"}[lvl]
    
    st.markdown(
        f"""
    <div style="background:#ffffff; border:1px solid rgba(2,6,23,0.08); border-radius:16px; padding:14px 16px;
                box-shadow:0 1px 2px rgba(2,6,23,0.05); margin-top:12px;">
        <div style="color: rgba(2,6,23,0.65); font-size:0.95rem;">Risk Meter (heuristic)</div>
        <div style="color:{color}; font-size:1.25rem; font-weight:900; margin-top:2px;">{lvl} risk</div>
        <div style="color: rgba(2,6,23,0.72); margin-top:6px;">Score: <b>{score}</b> (based on detected red-flag terms)</div>
    </div>
    """,
        unsafe_allow_html=True
    )

    if hits:
        st.caption("Detected terms: " + ", ".join(hits))

    st.download_button(
        "Download review as .md",
        data=md.encode("utf-8"),
        file_name="LegalEase_Review.md",
        mime="text/markdown",
    )
