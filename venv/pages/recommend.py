import streamlit as st
from common import sidebar, apply_base_style
from llm_reco import recommend_doc

apply_base_style()

jurisdiction, ack = sidebar()

st.title("Document Recommendation")
st.caption("Describe your situation. LegalEase suggests the most relevant legal document to generate.")

if not ack:
    st.warning("Please acknowledge the disclaimer in the sidebar to use this feature.")
    st.stop()

st.markdown(
    f"<span style='color: rgba(2, 6, 23, 0.65);'>Jurisdiction:</span> "
    f"<span style='color:#2563eb; font-weight:600;'>{jurisdiction}</span>",
    unsafe_allow_html=True
)

st.write("")

q = st.text_area(
    "What do you want to do?",
    placeholder="e.g., I want to hire a freelancer to build my website and protect my confidential info.",
    height=140
)

c1, c2 = st.columns([1, 1])
with c1:
    recommend_btn = st.button("Recommend document", type="primary")
with c2:
    clear_btn = st.button("Clear")

if clear_btn:
    st.rerun()

def bullet_list(items):
    if not items:
        return ""
    return "\n".join([f"- {x}" for x in items])

if recommend_btn:
    if not q.strip():
        st.warning("Write a short description first.")
        st.stop()

    with st.spinner("Analyzing…"):
        result = recommend_doc(q.strip(), jurisdiction)

    if "error" in result:
        st.error(result["error"])
        if "raw" in result:
            with st.expander("Show raw model output"):
                st.code(result["raw"])
        st.stop()

    st.write("")

    st.markdown(
        f"""
<div style="background:#ffffff; border:1px solid rgba(2,6,23,0.08); border-radius:16px; padding:16px 18px; box-shadow:0 1px 2px rgba(2,6,23,0.05);">
  <div style="color: rgba(2,6,23,0.65); font-size:0.9rem;">Recommended</div>
  <div style="color:#2563eb; font-size:1.25rem; font-weight:800; margin-top:2px;">
    {result.get("recommended_document","")}
  </div>
</div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    a1, a2 = st.columns(2)
    with a1:
        st.markdown("**Why this document**")
        st.markdown(bullet_list(result.get("why_this_document", [])) or "- (not provided)")
        st.write("")
        st.markdown("**Alternatives**")
        st.markdown(bullet_list(result.get("alternatives", [])) or "- (none)")

    with a2:
        st.markdown("**Required information to draft it**")
        st.markdown(bullet_list(result.get("required_information", [])) or "- (not provided)")
        st.write("")
        st.markdown("**Follow-up questions (if any)**")
        st.markdown(bullet_list(result.get("follow_up_questions", [])) or "- (none)")

    st.write("")
    st.markdown("**Risk notes / red flags**")
    st.markdown(bullet_list(result.get("risk_notes", [])) or "- (none)")

    # NEW: Continue to Draft (saves recommendation into session_state)
    st.write("")
    c3, c4 = st.columns([1, 1])
    with c3:
        if st.button("Continue to Draft", type="primary"):
            st.session_state["draft_doc_type"] = result.get("recommended_document", "")
            st.session_state["draft_required_info"] = result.get("required_information", [])
            st.session_state["draft_source_query"] = q.strip()
            try:
                st.switch_page("pages/draft.py")
            except Exception:
                st.success("Saved. Now open the Draft page from the left sidebar.")
    with c4:
        st.button("Edit query above")

    with st.expander("Show raw JSON"):
        st.json(result)
