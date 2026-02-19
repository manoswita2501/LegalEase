import streamlit as st
from common import sidebar, apply_base_style

apply_base_style()

jurisdiction, ack = sidebar()

st.title("Legal Resources")
st.caption("Official portals and reliable references, organized by topic (informational only).")

if not ack:
    st.warning("Please acknowledge the disclaimer in the sidebar to use this feature.")
    st.stop()

st.markdown(
    f"<span style='color: rgba(2, 6, 23, 0.65);'>Jurisdiction:</span> "
    f"<span style='color:#2563eb; font-weight:600;'>{jurisdiction}</span>",
    unsafe_allow_html=True
)

def card(title: str, desc: str, url: str, tags: list[str]):
    tag_html = " ".join(
        [f"<span style='display:inline-block; padding:2px 8px; border-radius:999px; "
         f"border:1px solid rgba(2,6,23,0.10); color: rgba(2,6,23,0.70); "
         f"font-size:0.80rem; margin-right:6px; background:#fff;'>{t}</span>" for t in tags]
    )

    st.markdown(
        f"""
<div style="background:#ffffff; border:1px solid rgba(2,6,23,0.08); border-radius:16px; padding:14px 16px;
            box-shadow:0 1px 2px rgba(2,6,23,0.05); margin-bottom:12px;">
  <div style="font-weight:800; font-size:1.05rem; color:#0f172a;">{title}</div>
  <div style="margin-top:6px; color: rgba(2,6,23,0.72); line-height:1.45;">{desc}</div>
  <div style="margin-top:10px;">{tag_html}</div>
  <div style="margin-top:10px;">
    <a href="{url}" target="_blank" style="text-decoration:none; font-weight:700; color:#2563eb;">Open resource →</a>
  </div>
</div>
""",
        unsafe_allow_html=True
    )

RESOURCES = {
    "India": [
        {
            "title": "NALSA – Apply for Free Legal Aid",
            "desc": "Apply for free legal aid (online/offline) via National Legal Services Authority. Useful if you can’t afford a lawyer.",
            "url": "https://nalsa.gov.in/legal-aid/",
            "tags": ["Legal Aid", "Government", "India"]
        },
        {
            "title": "NALSA Legal Aid Case Management System (LACMS)",
            "desc": "Online system for legal aid applications and case management under NALSA/NIC.",
            "url": "https://scourtapp.nic.in/lacms/",
            "tags": ["Legal Aid", "Portal", "India"]
        },
        {
            "title": "NALSA – Women’s Assistance",
            "desc": "Women-focused assistance resources, including helpline and legal aid guidance.",
            "url": "https://nalsa.gov.in/womens-assistance/",
            "tags": ["Women", "Legal Aid", "India"]
        },
        {
            "title": "eCourts Services – Case Status / Orders / Cause List",
            "desc": "Track case status, court orders, cause lists, etc. across courts in India (CNR-based lookup supported).",
            "url": "https://services.ecourts.gov.in/",
            "tags": ["Courts", "Case Status", "India"]
        },
        {
            "title": "National Consumer Helpline (NCH)",
            "desc": "File and track consumer grievances; access consumer guidance and support.",
            "url": "https://consumerhelpline.gov.in/",
            "tags": ["Consumer", "Complaint", "India"]
        },
        {
            "title": "RTI Online (DoPT) – File RTI Request/First Appeal",
            "desc": "Submit RTI requests and first appeals online (central ministries/departments covered).",
            "url": "https://rtionline.gov.in/",
            "tags": ["RTI", "Government", "India"]
        },
        {
            "title": "RTI Portal (rti.gov.in) – RTI Act + Online Services",
            "desc": "RTI Act reference + links to online services and state portals.",
            "url": "https://rti.gov.in/",
            "tags": ["RTI", "Act", "India"]
        },
        {
            "title": "india.gov.in – Service Directory (RTI / Consumer Complaint links)",
            "desc": "Government service directory that points to official portals (useful starting point).",
            "url": "https://services.india.gov.in/",
            "tags": ["Directory", "Government", "India"]
        },
    ],
    "General / Not specified": [
        {
            "title": "Start with your local legal aid authority / bar association",
            "desc": "If jurisdiction is unclear, look for official legal aid services or local bar association directories.",
            "url": "https://www.nalsa.gov.in/",  # safe fallback; user can change jurisdiction in sidebar
            "tags": ["General", "Legal Aid"]
        }
    ]
}

# Decide which list to show
key = jurisdiction if jurisdiction in RESOURCES else "General / Not specified"
items = RESOURCES.get(key, RESOURCES["General / Not specified"])

st.write("")
q = st.text_input("Search resources", placeholder="Try: RTI, consumer, case status, legal aid...")

all_tags = sorted({t for it in items for t in it["tags"]})
picked_tags = st.multiselect("Filter by tags", all_tags)

def ok(it):
    if q and q.strip():
        s = (it["title"] + " " + it["desc"] + " " + " ".join(it["tags"])).lower()
        if q.strip().lower() not in s:
            return False
    if picked_tags:
        if not any(t in it["tags"] for t in picked_tags):
            return False
    return True

shown = [it for it in items if ok(it)]

st.write("")
if not shown:
    st.info("No matches. Try clearing filters or using different keywords.")
else:
    for it in shown:
        card(it["title"], it["desc"], it["url"], it["tags"])

st.markdown("---")
st.markdown(
    "<div style='color: rgba(2,6,23,0.65); font-size:0.95rem; line-height:1.45;'>"
    "<b>Tip:</b> For urgent/high-stakes issues (criminal allegations, immigration deadlines, large financial exposure), "
    "use these portals to locate a licensed lawyer or legal aid provider in your jurisdiction."
    "<br><br>"
    "<i>Disclaimer: This is not legal advice.</i>"
    "</div>",
    unsafe_allow_html=True
)
