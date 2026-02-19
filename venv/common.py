import streamlit as st

def apply_base_style():
    st.markdown(
        """
<style>
/* Reduce top padding */
.block-container { padding-top: 1.1rem; }

/* Make text look cleaner */
html, body, [class*="css"]  { font-smoothing: antialiased; -webkit-font-smoothing: antialiased; }

/* Buttons: slightly rounded, cleaner */
.stButton button {
    border-radius: 12px !important;
    padding: 0.55rem 0.9rem !important;
    font-weight: 700 !important;
}

/* Inputs: rounded edges */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
    border-radius: 12px !important;
}

/* Caption color slightly softer */
[data-testid="stCaptionContainer"] { color: rgba(2, 6, 23, 0.65) !important; }
</style>
        """,
        unsafe_allow_html=True
    )

def sidebar():
    """
    Shared sidebar for all pages.
    Returns: (jurisdiction: str, ack: bool)
    """
    with st.sidebar:
        st.markdown("### **LegalEase**")
        st.markdown(
            "<span style='color:#2563eb; font-weight:700;'>AI Legal Assistant</span><br>"
            "<span style='color: rgba(2, 6, 23, 0.65);'>Informational only • Not a lawyer</span>",
            unsafe_allow_html=True
        )

        st.markdown("---")

        jurisdiction = st.selectbox(
            "Jurisdiction",
            ["India", "General / Not specified"],
            index=0
        )
        
        st.markdown(
            "<div style='color: rgba(2, 6, 23, 0.65); font-size:0.9rem; line-height:1.35;'>"
            "Choose <b>India</b> for India-specific context. Use <b>General</b> if you’re unsure."
            "</div>",
        unsafe_allow_html=True
        )


        ack = st.checkbox("I understand this is not legal advice.", value=False)

        st.markdown("---")
        st.markdown(
            "<div style='font-size:0.9rem; color: rgba(2, 6, 23, 0.65); line-height:1.35;'>"
            "LegalEase provides general information and drafting assistance. "
            "It does not create an attorney-client relationship. "
            "For urgent/high-stakes issues, consult a licensed attorney."
            "</div>",
            unsafe_allow_html=True
        )

    return jurisdiction, ack
