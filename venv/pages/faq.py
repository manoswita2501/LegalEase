import streamlit as st
from common import sidebar, apply_base_style
from llm_faq import answer_faq

apply_base_style()

jurisdiction, ack = sidebar()

st.title("FAQ & Knowledge Base")
st.caption("Common legal questions explained simply (informational only).")

if not ack:
    st.warning("Please acknowledge the disclaimer in the sidebar to use this feature.")
    st.stop()

st.markdown(
    f"<span style='color: rgba(2, 6, 23, 0.65);'>Jurisdiction:</span> "
    f"<span style='color:#2563eb; font-weight:600;'>{jurisdiction}</span>",
    unsafe_allow_html=True
)

FAQ_BANK = {
    "Contracts & Agreements": [
        "What makes a contract legally valid?",
        "What should I check before signing an NDA?",
        "What are common red flags in freelance/service agreements?",
        "What does 'termination for convenience' mean?",
        "What does 'limitation of liability' mean in simple terms?",
    ],
    "Employment": [
        "What should an offer letter include?",
        "What is probation/trial period and what should I clarify?",
        "What are common issues in employment contracts?",
    ],
    "Payments & Disputes": [
        "What should I do if someone is not paying an invoice?",
        "How do I write a notice/demand letter without escalating too hard?",
        "What evidence should I keep for a payment dispute?",
    ],
    "Privacy & Data": [
        "What is personal data and why does it matter in agreements?",
        "What clauses should be in a simple privacy policy (high-level)?",
    ],
}

st.write("")
query = st.text_input("Search questions", placeholder="Type keywords like 'NDA', 'invoice', 'probation'...")

def matches(q: str, s: str) -> bool:
    q = (q or "").strip().lower()
    if not q:
        return True
    return q in s.lower()

picked = None
for section, qs in FAQ_BANK.items():
    visible = [x for x in qs if matches(query, x)]
    if not visible:
        continue
    with st.expander(section, expanded=True if query else False):
        for q in visible:
            if st.button(q, use_container_width=True):
                picked = q
                st.session_state["faq_q"] = q

st.write("")
st.markdown("---")
st.subheader("Ask your own question")

custom_q = st.text_area("Question", height=90, placeholder="Type your legal question here (general info only).")
c1, c2 = st.columns([1, 1])
with c1:
    ask_btn = st.button("Get answer", type="primary")
with c2:
    clear_btn = st.button("Clear")

if clear_btn:
    st.session_state.pop("faq_answer_md", None)
    st.session_state.pop("faq_q", None)
    st.rerun()

final_q = ""
if ask_btn:
    final_q = custom_q.strip()
elif "faq_q" in st.session_state:
    final_q = st.session_state["faq_q"]

if final_q:
    with st.spinner("Thinking…"):
        md = answer_faq(final_q, jurisdiction)
    st.session_state["faq_answer_md"] = md
    st.session_state["faq_q"] = final_q

md = st.session_state.get("faq_answer_md", "")
if md:
    st.write("")
    st.markdown("### Answer")
    st.markdown(md)

    st.download_button(
        "Download answer as .md",
        data=md.encode("utf-8"),
        file_name="LegalEase_FAQ_Answer.md",
        mime="text/markdown",
    )
