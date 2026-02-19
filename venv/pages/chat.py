import streamlit as st
from common import sidebar, apply_base_style
from llm_chat import ask_gemini

apply_base_style()

jurisdiction, ack = sidebar()

st.title("Chat")
st.caption("General legal information (not legal advice).")

if not ack:
    st.warning("Please acknowledge the disclaimer in the sidebar to use Chat.")
    st.stop()

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

st.markdown(
    f"<span style='color: rgba(2, 6, 23, 0.65);'>Jurisdiction:</span> "
    f"<span style='color:#2563eb; font-weight:600;'>{jurisdiction}</span>",
    unsafe_allow_html=True
)

st.write("")

for m in st.session_state["chat_messages"]:
    with st.chat_message(m["role"]):
        st.write(m["content"])

user_msg = st.chat_input("Ask something legal (e.g., 'What should be in a mutual NDA?')")

if user_msg:
    # Save + render user message immediately
    st.session_state["chat_messages"].append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.write(user_msg)

    # Generate + render assistant message
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            ans = ask_gemini(user_msg, jurisdiction)
            st.write(ans)

    st.session_state["chat_messages"].append({"role": "assistant", "content": ans})


st.markdown("---")
if st.button("Clear chat"):
    st.session_state["chat_messages"] = []
    st.rerun()
