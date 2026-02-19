import streamlit as st
from common import sidebar, apply_base_style
from datetime import date
from llm_draft import polish_markdown, draft_custom_markdown

apply_base_style()

jurisdiction, ack = sidebar()

st.title("Draft")
st.caption("Fill in details → generate a draft document (not legal advice).")

if not ack:
    st.warning("Please acknowledge the disclaimer in the sidebar to use Draft.")
    st.stop()


def render_nda(d: dict, jurisdiction: str) -> str:
    doc_type = d.get("doc_type", "Mutual NDA")
    party_a = (d.get("party_a") or "[Party A]").strip()
    party_b = (d.get("party_b") or "[Party B]").strip()
    purpose = (d.get("purpose") or "Evaluate a potential business relationship").strip()
    term = (d.get("term") or "2 years").strip()
    governing = (d.get("governing") or jurisdiction or "General / Not specified").strip()

    mutual = (doc_type == "Mutual NDA")
    today = date.today().strftime("%B %d, %Y")

    title = "MUTUAL NON-DISCLOSURE AGREEMENT" if mutual else "NON-DISCLOSURE AGREEMENT (ONE-WAY)"
    disclosing = "each party" if mutual else "the Disclosing Party"
    receiving = "each party" if mutual else "the Receiving Party"

    opt_compelled = bool(d.get("opt_compelled_disclosure"))
    opt_non_solicit = bool(d.get("opt_non_solicit"))
    opt_non_compete = bool(d.get("opt_non_compete"))
    opt_no_assignment = bool(d.get("opt_no_assignment"))
    opt_no_publicity = bool(d.get("opt_no_publicity"))

    optional_sections = []

    if opt_compelled:
        optional_sections.append(
            """
## Additional Clause: Compelled Disclosure
If the Receiving Party is required by law, regulation, or court order to disclose any Confidential Information, it may do so **only to the extent required**, provided that (to the extent legally permitted) it gives the Disclosing Party prompt written notice and reasonably cooperates (at the Disclosing Party’s expense) in seeking protective treatment.
            """.strip()
        )

    if opt_non_solicit:
        optional_sections.append(
            """
## Additional Clause: Non-Solicitation
For the term of this Agreement and for **12 months** thereafter, the Receiving Party shall not knowingly solicit for employment or engagement the Disclosing Party’s employees or contractors that it became aware of through the Purpose, except through general advertisements not targeted at such persons.
            """.strip()
        )

    if opt_non_compete:
        optional_sections.append(
            """
## Additional Clause: Limited Non-Compete (Optional)
**Note:** Enforceability of non-compete obligations varies significantly by jurisdiction. Consider legal review.
For the term of this Agreement and for **6 months** thereafter, the Receiving Party agrees not to use Confidential Information to build a directly competing product/service substantially similar to what was disclosed for the Purpose.
            """.strip()
        )

    if opt_no_publicity:
        optional_sections.append(
            """
## Additional Clause: No Publicity
Neither Party shall issue public statements or use the other Party’s name, logo, or trademarks in any publicity or marketing materials regarding the Purpose without prior written consent.
            """.strip()
        )

    if opt_no_assignment:
        optional_sections.append(
            """
## Additional Clause: No Assignment
Neither Party may assign or transfer this Agreement without the prior written consent of the other Party, except to a successor in connection with a merger, acquisition, or sale of substantially all assets, provided the successor is bound by this Agreement.
            """.strip()
        )

    optional_block = ""
    if optional_sections:
        optional_block = "\n\n---\n\n# Optional Clauses Included\n\n" + "\n\n".join(optional_sections)

    md = f"""
# {title}

**Effective Date:** {today}

This {title} (“**Agreement**”) is entered into by and between **{party_a}** and **{party_b}** (each a “**Party**”, and together the “**Parties**”).

## 1. Purpose
The Parties wish to disclose certain confidential information for the purpose of: **{purpose}** (“**Purpose**”). The {receiving} agrees to receive, protect, and use such information only as permitted under this Agreement.

## 2. Definition of Confidential Information
“**Confidential Information**” means any non-public information disclosed by **{disclosing}** to the other, whether in written, oral, visual, electronic, or other form, that is designated as confidential or that reasonably should be understood to be confidential given the nature of the information and the circumstances of disclosure.

## 3. Exclusions
Confidential Information does not include information that the Receiving Party can demonstrate:
- is or becomes publicly available through no breach of this Agreement;
- was lawfully known to the Receiving Party prior to disclosure;
- is lawfully received from a third party without restriction;
- is independently developed without use of Confidential Information.

## 4. Obligations of the Receiving Party
The Receiving Party shall:
- use Confidential Information solely for the Purpose;
- not disclose Confidential Information to any third party except to permitted recipients under Section 5;
- protect Confidential Information using at least reasonable care (and no less than the care used to protect its own similar information);
- promptly notify the Disclosing Party if it becomes aware of unauthorized disclosure.

## 5. Permitted Recipients
The Receiving Party may disclose Confidential Information to its employees, contractors, or advisors who have a legitimate need to know for the Purpose and are bound by confidentiality obligations at least as protective as this Agreement.

## 6. Term and Survival
This Agreement remains in effect until terminated by either Party with written notice. The confidentiality obligations will continue for **{term}** from the date of disclosure of the Confidential Information.

## 7. Return or Destruction
Upon written request, the Receiving Party will return or destroy all Confidential Information, except that one archival copy may be retained for legal/compliance purposes.

## 8. No License
No rights or licenses are granted under this Agreement by implication or otherwise, except as expressly stated.

## 9. Remedies
The Parties acknowledge that unauthorized disclosure may cause irreparable harm for which monetary damages may be insufficient, and injunctive relief may be appropriate.

## 10. Governing Law
This Agreement shall be governed by the laws of **{governing}**, without regard to conflict of law principles.

## 11. Entire Agreement
This Agreement constitutes the entire agreement between the Parties regarding the subject matter and supersedes prior discussions or agreements relating to Confidential Information.

---

### Signatures

**{party_a}**
Name: __________________________
Title: __________________________
Date: __________________________

**{party_b}**
Name: __________________________
Title: __________________________
Date: __________________________

---

*Disclaimer: LegalEase provides general information and drafting assistance only; this is not legal advice.*
{optional_block}
    """.strip()

    return md


def render_service_agreement(d: dict, jurisdiction: str) -> str:
    client = (d.get("client") or "[Client]").strip()
    contractor = (d.get("contractor") or "[Contractor]").strip()
    services = (d.get("services") or "Provide professional services as described in Exhibit A.").strip()
    deliverables = (d.get("deliverables") or "As agreed between the Parties in writing.").strip()
    start_date = (d.get("start_date") or "Effective Date").strip()
    end_date = (d.get("end_date") or "Completion of Services").strip()
    fee_type = d.get("fee_type") or "Fixed"
    fee_amount = (d.get("fee_amount") or "").strip()
    payment_terms = (d.get("payment_terms") or "Net 15 days from invoice date.").strip()
    governing = (d.get("governing") or jurisdiction or "General / Not specified").strip()

    opt_ip = d.get("opt_ip") or "Client owns deliverables"
    opt_conf = bool(d.get("opt_confidentiality"))
    opt_termination = bool(d.get("opt_termination"))
    notice_days = (d.get("notice_days") or "7").strip()
    opt_lim_liab = bool(d.get("opt_lim_liability"))
    liability_cap = (d.get("liability_cap") or "Fees paid in the last 3 months").strip()
    opt_non_solicit = bool(d.get("opt_sa_non_solicit"))

    today = date.today().strftime("%B %d, %Y")

    fee_line = ""
    if fee_type == "Fixed":
        fee_line = f"**Fee:** Fixed fee of **{fee_amount or '[Amount]'}**."
    elif fee_type == "Hourly":
        fee_line = f"**Fee:** Hourly rate of **{fee_amount or '[Rate]'}** per hour."
    else:
        fee_line = f"**Fee:** Milestone-based payments totaling **{fee_amount or '[Amount]'}**."

    ip_clause = ""
    if opt_ip == "Client owns deliverables":
        ip_clause = """
## 6. Intellectual Property
Upon full payment, Contractor assigns to Client all right, title, and interest in the deliverables created specifically for Client under this Agreement, excluding Contractor’s pre-existing materials and general know-how.
        """.strip()
    elif opt_ip == "Contractor owns; Client gets license":
        ip_clause = """
## 6. Intellectual Property
Contractor retains ownership of the work product and grants Client a perpetual, non-exclusive, worldwide license to use the deliverables for Client’s internal business purposes, subject to full payment.
        """.strip()
    else:
        ip_clause = """
## 6. Intellectual Property
Ownership of deliverables will be as specified in Exhibit A or a written statement of work signed by both Parties.
        """.strip()

    conf_clause = ""
    if opt_conf:
        conf_clause = """
## 7. Confidentiality
Each Party may receive confidential information from the other. The Receiving Party agrees to protect such information using reasonable care and to use it only for purposes of this Agreement. This obligation survives termination for **2 years**.
        """.strip()

    term_clause = ""
    if opt_termination:
        term_clause = f"""
## 9. Termination
Either Party may terminate this Agreement for convenience with **{notice_days}** days’ written notice. Upon termination, Client shall pay for services performed and approved expenses incurred up to the effective termination date.
        """.strip()

    lim_liab_clause = ""
    if opt_lim_liab:
        lim_liab_clause = f"""
## 10. Limitation of Liability
To the maximum extent permitted by law, neither Party shall be liable for indirect, incidental, special, or consequential damages. Each Party’s total liability under this Agreement shall not exceed **{liability_cap}**.
        """.strip()

    non_solicit_clause = ""
    if opt_non_solicit:
        non_solicit_clause = """
## 11. Non-Solicitation (Optional)
For the term of this Agreement and for **12 months** thereafter, neither Party shall knowingly solicit for employment the other Party’s personnel who were materially involved in the Services, except through general advertisements not targeted at such personnel.
        """.strip()

    md = f"""
# SERVICE AGREEMENT / FREELANCE CONTRACT

**Effective Date:** {today}

This Service Agreement (“**Agreement**”) is between **{client}** (“**Client**”) and **{contractor}** (“**Contractor**”).

## 1. Services
Contractor will perform the following services: **{services}**

## 2. Deliverables
Expected deliverables: **{deliverables}**

## 3. Term
Start: **{start_date}**  
End: **{end_date}** (or earlier termination under this Agreement)

## 4. Fees and Payment
{fee_line}  
**Payment terms:** {payment_terms}  
Contractor will invoice Client as agreed (e.g., weekly, monthly, or per milestone). Client is responsible for any applicable taxes required by law.

## 5. Independent Contractor
Contractor is an independent contractor and not an employee, partner, or agent of Client. Contractor is responsible for their own taxes, insurance, and compliance obligations.

{ip_clause}

## 8. Warranties
Contractor represents that (i) they have the right to enter this Agreement, and (ii) to the best of their knowledge, deliverables will not knowingly infringe third-party rights. Except as stated, services are provided “as is” to the extent permitted by law.

{conf_clause}

## 9. Compliance
Each Party will comply with applicable laws relevant to performance under this Agreement.

{term_clause}

{lim_liab_clause}

{non_solicit_clause}

## 12. Governing Law
This Agreement shall be governed by the laws of **{governing}**, without regard to conflict of law principles.

## 13. Entire Agreement
This Agreement is the entire agreement between the Parties regarding the Services and supersedes prior discussions.

---

### Signatures

**{client}**  
Name: __________________________  
Title: __________________________  
Date: __________________________  

**{contractor}**  
Name: __________________________  
Title: __________________________  
Date: __________________________  

---

Disclaimer: LegalEase provides general information and drafting assistance only; this is not legal advice.
    """.strip()

    return md

def render_offer_letter(d: dict, jurisdiction: str) -> str:
    company = (d.get("company") or "[Company]").strip()
    candidate = (d.get("candidate") or "[Candidate]").strip()
    role = (d.get("role") or "Software Engineer").strip()
    start_date = (d.get("ol_start_date") or "To be mutually agreed").strip()
    location = (d.get("location") or "Remote / Hybrid").strip()
    manager = (d.get("manager") or "[Manager]").strip()
    employment_type = (d.get("employment_type") or "Full-time").strip()
    probation = (d.get("probation") or "3 months").strip()

    salary = (d.get("salary") or "[Compensation]").strip()
    pay_frequency = (d.get("pay_frequency") or "monthly").strip()
    bonus = (d.get("bonus") or "N/A").strip()
    benefits = (d.get("benefits") or "Standard company benefits as applicable.").strip()

    notice = (d.get("notice") or "as per applicable law / company policy").strip()
    governing = (d.get("governing") or jurisdiction or "General / Not specified").strip()

    opt_at_will = bool(d.get("opt_at_will"))
    opt_bg_check = bool(d.get("opt_bg_check"))
    opt_conf = bool(d.get("opt_ol_conf"))
    opt_ip = bool(d.get("opt_ol_ip"))
    opt_nca = bool(d.get("opt_ol_nca"))

    today = date.today().strftime("%B %d, %Y")

    at_will_clause = ""
    if opt_at_will:
        at_will_clause = """
## Employment Relationship (At-Will)
If applicable in your jurisdiction, your employment will be “at-will,” meaning either you or the Company may end the employment relationship at any time, with or without cause, subject to applicable law.
        """.strip()

    bg_clause = ""
    if opt_bg_check:
        bg_clause = """
## Background / Verification
This offer is contingent upon successful completion of reference checks and any background or verification processes permitted by law.
        """.strip()

    conf_clause = ""
    if opt_conf:
        conf_clause = """
## Confidentiality
You agree to protect the Company’s confidential information and comply with all confidentiality policies and agreements you may sign as a condition of employment.
        """.strip()

    ip_clause = ""
    if opt_ip:
        ip_clause = """
## Intellectual Property
You agree that intellectual property created within the scope of your employment or using Company resources belongs to the Company, subject to applicable law and any separate invention assignment agreement.
        """.strip()

    nca_clause = ""
    if opt_nca:
        nca_clause = """
## Restrictive Covenants (Optional)
Certain jurisdictions restrict non-compete obligations. If applicable, any restrictive covenants (non-compete/non-solicit) will be governed by a separate agreement and applicable law.
        """.strip()

    md = f"""
# EMPLOYMENT OFFER LETTER

**Date:** {today}

**To:** {candidate}  
**From:** {company}

Dear {candidate},

We are pleased to offer you the position of **{role}** with **{company}** on a **{employment_type}** basis.

## 1. Reporting & Work Location
- **Reporting to:** {manager}  
- **Work location:** {location}  
- **Proposed start date:** {start_date}

## 2. Compensation
- **Salary/Compensation:** {salary} (paid {pay_frequency})  
- **Bonus/Incentives:** {bonus}  
- **Benefits:** {benefits}

## 3. Probation / Initial Period
Your employment will be subject to an initial probation/trial period of **{probation}**, during which performance and fit may be evaluated, subject to applicable law.

## 4. Notice / Termination
Termination and notice requirements will be **{notice}**, subject to applicable law and Company policy.

{at_will_clause}

{bg_clause}

{conf_clause}

{ip_clause}

{nca_clause}

## 5. Policies & Documents
Your employment is subject to Company policies and the execution of any required documents (e.g., confidentiality, code of conduct, IP assignment), as applicable.

## 6. Governing Law
This offer letter will be governed by the laws of **{governing}**, to the extent permitted.

---

### Acceptance

If you accept this offer, please sign below and return a copy.

**For {company}**  
Name: __________________________  
Title: __________________________  
Date: __________________________  

**Accepted by {candidate}**  
Signature: ______________________  
Name: ___________________________  
Date: ___________________________  

---

Disclaimer: LegalEase provides general information and drafting assistance only; this is not legal advice.
    """.strip()

    return md

def render_notice_letter(d: dict, jurisdiction: str) -> str:
    sender = (d.get("sender") or "[Sender Name]").strip()
    sender_addr = (d.get("sender_addr") or "[Sender Address]").strip()
    sender_email = (d.get("sender_email") or "[Sender Email]").strip()

    recipient = (d.get("recipient") or "[Recipient Name]").strip()
    recipient_addr = (d.get("recipient_addr") or "[Recipient Address]").strip()

    subject = (d.get("subject") or "Legal Notice / Demand").strip()
    relationship = (d.get("relationship") or "The parties had a prior relationship/transaction.").strip()
    issue = (d.get("issue") or "Describe the issue clearly and factually.").strip()
    demand = (d.get("demand") or "State what you want the recipient to do.").strip()
    deadline = (d.get("deadline") or "7").strip()
    amount = (d.get("amount") or "N/A").strip()
    evidence = (d.get("evidence") or "Relevant emails, invoices, messages, agreements, screenshots.").strip()

    tone = (d.get("tone") or "Firm").strip()
    governing = (d.get("governing") or jurisdiction or "General / Not specified").strip()

    opt_without_prejudice = bool(d.get("opt_without_prejudice"))
    opt_payment_plan = bool(d.get("opt_payment_plan"))
    opt_preserve_evidence = bool(d.get("opt_preserve_evidence"))

    today = date.today().strftime("%B %d, %Y")

    tone_line = {
        "Polite": "This letter is sent in good faith to resolve the matter amicably.",
        "Firm": "This letter is sent to formally notify you of the issue and request prompt resolution.",
        "Aggressive": "This letter serves as a final notice before escalation, subject to applicable law.",
    }.get(tone, "This letter is sent to request prompt resolution.")

    wp_line = ""
    if opt_without_prejudice:
        wp_line = "**Without Prejudice:** This communication is made without prejudice to the Sender’s rights and remedies."

    payment_plan_line = ""
    if opt_payment_plan:
        payment_plan_line = (
            "- If you are unable to pay the full amount immediately, propose a written payment plan within the deadline.\n"
        )

    preserve_line = ""
    if opt_preserve_evidence:
        preserve_line = (
            "- Preserve all records relevant to this matter (emails, messages, logs, contracts, invoices). Deletion may have legal consequences.\n"
        )

    amount_block = ""
    if amount and amount.strip().lower() != "n/a":
        amount_block = f"**Amount involved (if applicable):** {amount}\n"

    md = f"""
# DEMAND / NOTICE LETTER

**Date:** {today}

**From:** {sender}  
{sender_addr}  
Email: {sender_email}  

**To:** {recipient}  
{recipient_addr}  

**Subject:** {subject}

{wp_line}

---

## 1. Background
{tone_line}

**Relationship/Context:** {relationship}

## 2. Issue / Breach
{issue}

{amount_block}

## 3. Demand
I/we hereby request that you do the following:

- {demand}
{payment_plan_line}{preserve_line}

## 4. Deadline
Please comply **within {deadline} days** of receipt of this notice. If you fail to comply within this time, I/we may consider pursuing appropriate remedies available under applicable law, including formal dispute resolution.

## 5. Supporting Information
Evidence/documents that support this matter may include:
{evidence}

## 6. Governing Law / Jurisdiction
This notice is issued with reference to the laws of **{governing}**, to the extent applicable.

---

Sincerely,  
**{sender}**

---

Disclaimer: LegalEase provides general information and drafting assistance only; this is not legal advice.
""".strip()

    return md



# Pull recommendation from Page 2 if available
rec_doc = st.session_state.get("draft_doc_type", "")
src_q = st.session_state.get("draft_source_query", "")

st.markdown(
    f"<span style='color: rgba(2, 6, 23, 0.65);'>Jurisdiction:</span> "
    f"<span style='color:#2563eb; font-weight:600;'>{jurisdiction}</span>",
    unsafe_allow_html=True
)

if rec_doc:
    st.write("")
    st.markdown(
        f"""
<div style="background:#ffffff; border:1px solid rgba(2,6,23,0.08); border-radius:16px; padding:14px 16px; box-shadow:0 1px 2px rgba(2,6,23,0.05);">
  <div style="color: rgba(2,6,23,0.65); font-size:0.9rem;">Recommended from Document Recommendation</div>
  <div style="color:#2563eb; font-size:1.1rem; font-weight:800; margin-top:2px;">{rec_doc}</div>
</div>
        """,
        unsafe_allow_html=True
    )
    if src_q:
        st.caption(f"Based on: {src_q}")

st.write("")

doc_choices = [
    "Mutual NDA",
    "One-way NDA",
    "Service Agreement / Freelance Contract",
    "Employment Offer Letter",
    "Demand / Notice Letter",
    "Other (custom)",
]

default_idx = doc_choices.index(rec_doc) if rec_doc in doc_choices else 0
doc_type = st.selectbox("Select document type to draft", doc_choices, index=default_idx)

st.write("")

draft_md = ""

# ---------------- NDA ----------------
if doc_type in ["Mutual NDA", "One-way NDA"]:
    st.subheader("NDA details")

    with st.form("nda_form"):
        c1, c2 = st.columns(2)
        with c1:
            party_a = st.text_input("Party A (Name)")
        with c2:
            party_b = st.text_input("Party B (Name)")

        purpose = st.text_input("Purpose of disclosure", value="Evaluate a potential business relationship")
        term = st.selectbox("Confidentiality term", ["6 months", "1 year", "2 years", "3 years", "5 years"], index=2)
        governing = st.text_input("Governing law (optional)", placeholder="e.g., India (West Bengal)")

        with st.expander("Optional clauses (customize)"):
            st.markdown(
                "<span style='color: rgba(2,6,23,0.65);'>Toggle clauses to include in the draft.</span>",
                unsafe_allow_html=True,
            )
            opt_compelled = st.checkbox("Compelled disclosure clause (court/order disclosure)", value=True)
            opt_non_solicit = st.checkbox("Non-solicitation (12 months)", value=False)
            opt_non_compete = st.checkbox("Limited non-compete (⚠ jurisdiction-sensitive)", value=False)
            opt_no_publicity = st.checkbox("No publicity / no use of name/logo", value=True)
            opt_no_assignment = st.checkbox("No assignment without consent", value=True)

        submitted = st.form_submit_button("Save details")
        if submitted:
            st.session_state["draft_inputs"] = {
                "doc_type": doc_type,
                "party_a": party_a,
                "party_b": party_b,
                "purpose": purpose,
                "term": term,
                "governing": governing,
                "opt_compelled_disclosure": opt_compelled,
                "opt_non_solicit": opt_non_solicit,
                "opt_non_compete": opt_non_compete,
                "opt_no_publicity": opt_no_publicity,
                "opt_no_assignment": opt_no_assignment,
            }
            st.success("Saved. You can generate the draft below.")

    st.write("")

    if "draft_inputs" in st.session_state and st.session_state["draft_inputs"].get("doc_type") in ["Mutual NDA", "One-way NDA"]:
        c3, c4 = st.columns([1, 1])
        with c3:
            gen = st.button("Generate draft", type="primary")
        with c4:
            if st.button("Reset saved details"):
                st.session_state.pop("draft_inputs", None)
                st.session_state.pop("draft_preview_md", None)
                st.rerun()

        if gen:
            draft_md = render_nda(st.session_state["draft_inputs"], jurisdiction)
            st.session_state["draft_preview_md"] = draft_md

        draft_md = st.session_state.get("draft_preview_md", "")

# -------- Service Agreement / Freelance Contract --------
elif doc_type == "Service Agreement / Freelance Contract":
    st.subheader("Service Agreement details")

    with st.form("sa_form"):
        c1, c2 = st.columns(2)
        with c1:
            client = st.text_input("Client (Name)")
        with c2:
            contractor = st.text_input("Contractor / Freelancer (Name)")

        services = st.text_area("Services description", placeholder="e.g., Build a Streamlit web app with Gemini integration.", height=90)
        deliverables = st.text_area("Deliverables", placeholder="e.g., Source code repo, deployment guide, 2 rounds of revisions.", height=90)

        c3, c4 = st.columns(2)
        with c3:
            start_date = st.text_input("Start date", placeholder="e.g., March 1, 2026")
        with c4:
            end_date = st.text_input("End date / expected completion", placeholder="e.g., April 15, 2026")

        c5, c6, c7 = st.columns(3)
        with c5:
            fee_type = st.selectbox("Fee type", ["Fixed", "Hourly", "Milestone"], index=0)
        with c6:
            fee_amount = st.text_input("Amount / Rate", placeholder="e.g., ₹50,000 or $40/hour")
        with c7:
            payment_terms = st.text_input("Payment terms", value="Net 15 days from invoice date.")

        governing = st.text_input("Governing law (optional)", placeholder="e.g., India (West Bengal)")

        with st.expander("Optional clauses (customize)"):
            st.markdown(
                "<span style='color: rgba(2,6,23,0.65);'>Toggle clauses to include in the draft.</span>",
                unsafe_allow_html=True,
            )
            opt_ip = st.selectbox(
                "IP ownership",
                ["Client owns deliverables", "Contractor owns; Client gets license", "As specified in Exhibit A"],
                index=0,
            )
            opt_confidentiality = st.checkbox("Include confidentiality clause", value=True)
            opt_termination = st.checkbox("Include termination for convenience", value=True)
            notice_days = st.text_input("Termination notice days", value="7")
            opt_lim_liability = st.checkbox("Include limitation of liability", value=True)
            liability_cap = st.text_input("Liability cap", value="Fees paid in the last 3 months")
            opt_sa_non_solicit = st.checkbox("Include non-solicitation (12 months)", value=False)

        submitted = st.form_submit_button("Save details")
        if submitted:
            st.session_state["draft_inputs"] = {
                "doc_type": doc_type,
                "client": client,
                "contractor": contractor,
                "services": services,
                "deliverables": deliverables,
                "start_date": start_date,
                "end_date": end_date,
                "fee_type": fee_type,
                "fee_amount": fee_amount,
                "payment_terms": payment_terms,
                "governing": governing,
                "opt_ip": opt_ip,
                "opt_confidentiality": opt_confidentiality,
                "opt_termination": opt_termination,
                "notice_days": notice_days,
                "opt_lim_liability": opt_lim_liability,
                "liability_cap": liability_cap,
                "opt_sa_non_solicit": opt_sa_non_solicit,
            }
            st.success("Saved. You can generate the draft below.")

    st.write("")

    if "draft_inputs" in st.session_state and st.session_state["draft_inputs"].get("doc_type") == "Service Agreement / Freelance Contract":
        c3, c4 = st.columns([1, 1])
        with c3:
            gen = st.button("Generate draft", type="primary")
        with c4:
            if st.button("Reset saved details"):
                st.session_state.pop("draft_inputs", None)
                st.session_state.pop("draft_preview_md", None)
                st.rerun()

        if gen:
            draft_md = render_service_agreement(st.session_state["draft_inputs"], jurisdiction)
            st.session_state["draft_preview_md"] = draft_md

        draft_md = st.session_state.get("draft_preview_md", "")

# -------- Employment Offer Letter --------
elif doc_type == "Employment Offer Letter":
    st.subheader("Employment Offer Letter details")

    with st.form("ol_form"):
        c1, c2 = st.columns(2)
        with c1:
            company = st.text_input("Company (Name)")
        with c2:
            candidate = st.text_input("Candidate (Name)")

        c3, c4 = st.columns(2)
        with c3:
            role = st.text_input("Role / Position", value="Software Engineer")
        with c4:
            employment_type = st.selectbox("Employment type", ["Full-time", "Part-time", "Contract"], index=0)

        c5, c6 = st.columns(2)
        with c5:
            ol_start_date = st.text_input("Start date", placeholder="e.g., March 10, 2026")
        with c6:
            location = st.text_input("Work location", placeholder="e.g., Mumbai / Remote / Hybrid")

        manager = st.text_input("Reporting manager", placeholder="e.g., Engineering Manager")

        c7, c8 = st.columns(2)
        with c7:
            salary = st.text_input("Salary / Compensation", placeholder="e.g., ₹12 LPA or $120,000/year")
        with c8:
            pay_frequency = st.selectbox("Pay frequency", ["monthly", "bi-weekly", "weekly"], index=0)

        bonus = st.text_input("Bonus / Incentives (optional)", value="N/A")
        benefits = st.text_area("Benefits (optional)", value="Standard company benefits as applicable.", height=70)

        c9, c10 = st.columns(2)
        with c9:
            probation = st.text_input("Probation / trial period", value="3 months")
        with c10:
            notice = st.text_input("Notice / termination terms", value="as per applicable law / company policy")

        governing = st.text_input("Governing law (optional)", placeholder="e.g., India (Maharashtra)")

        with st.expander("Optional clauses (customize)"):
            st.markdown(
                "<span style='color: rgba(2,6,23,0.65);'>Toggle clauses to include in the letter.</span>",
                unsafe_allow_html=True,
            )
            opt_at_will = st.checkbox("At-will employment clause (if applicable)", value=False)
            opt_bg_check = st.checkbox("Background / verification contingency", value=True)
            opt_ol_conf = st.checkbox("Confidentiality reference", value=True)
            opt_ol_ip = st.checkbox("IP ownership reference", value=True)
            opt_ol_nca = st.checkbox("Restrictive covenants note (jurisdiction-sensitive)", value=False)

        submitted = st.form_submit_button("Save details")
        if submitted:
            st.session_state["draft_inputs"] = {
                "doc_type": doc_type,
                "company": company,
                "candidate": candidate,
                "role": role,
                "employment_type": employment_type,
                "ol_start_date": ol_start_date,
                "location": location,
                "manager": manager,
                "salary": salary,
                "pay_frequency": pay_frequency,
                "bonus": bonus,
                "benefits": benefits,
                "probation": probation,
                "notice": notice,
                "governing": governing,
                "opt_at_will": opt_at_will,
                "opt_bg_check": opt_bg_check,
                "opt_ol_conf": opt_ol_conf,
                "opt_ol_ip": opt_ol_ip,
                "opt_ol_nca": opt_ol_nca,
            }
            st.success("Saved. You can generate the draft below.")

    st.write("")

    if "draft_inputs" in st.session_state and st.session_state["draft_inputs"].get("doc_type") == "Employment Offer Letter":
        c3, c4 = st.columns([1, 1])
        with c3:
            gen = st.button("Generate draft", type="primary")
        with c4:
            if st.button("Reset saved details"):
                st.session_state.pop("draft_inputs", None)
                st.session_state.pop("draft_preview_md", None)
                st.rerun()

        if gen:
            draft_md = render_offer_letter(st.session_state["draft_inputs"], jurisdiction)
            st.session_state["draft_preview_md"] = draft_md

        draft_md = st.session_state.get("draft_preview_md", "")

# -------- Demand / Notice Letter --------
elif doc_type == "Demand / Notice Letter":
    st.subheader("Demand / Notice Letter details")

    with st.form("notice_form"):
        st.markdown("**Sender details**")
        sender = st.text_input("Sender name")
        sender_addr = st.text_area("Sender address", height=60)
        sender_email = st.text_input("Sender email")

        st.write("")
        st.markdown("**Recipient details**")
        recipient = st.text_input("Recipient name")
        recipient_addr = st.text_area("Recipient address", height=60)

        st.write("")
        subject = st.text_input("Subject", value="Legal Notice / Demand for Resolution")

        tone = st.selectbox("Tone", ["Polite", "Firm", "Aggressive"], index=1)

        relationship = st.text_area(
            "Relationship / context",
            placeholder="e.g., I paid an advance for a service on Jan 10. Work was not delivered.",
            height=80,
        )
        issue = st.text_area(
            "Issue / breach (facts only)",
            placeholder="e.g., Despite reminders on Feb 1 and Feb 5, service was not delivered and no refund was issued.",
            height=110,
        )

        c1, c2 = st.columns(2)
        with c1:
            amount = st.text_input("Amount involved (optional)", placeholder="e.g., ₹25,000")
        with c2:
            deadline = st.text_input("Deadline (days)", value="7")

        demand = st.text_area(
            "What do you demand?",
            placeholder="e.g., Refund the full amount and confirm cancellation in writing.",
            height=80,
        )

        evidence = st.text_area(
            "Supporting documents / evidence list (bullets are fine)",
            value="- Emails/WhatsApp messages\n- Invoice/receipt\n- Contract/quotation\n- Screenshots",
            height=90,
        )

        governing = st.text_input("Governing law (optional)", placeholder="e.g., India (Maharashtra)")

        with st.expander("Optional clauses (customize)"):
            st.markdown(
                "<span style='color: rgba(2,6,23,0.65);'>Toggle clauses to include in the letter.</span>",
                unsafe_allow_html=True,
            )
            opt_without_prejudice = st.checkbox("Add 'Without Prejudice' line", value=True)
            opt_payment_plan = st.checkbox("Offer payment plan option (if money involved)", value=False)
            opt_preserve_evidence = st.checkbox("Ask recipient to preserve evidence", value=True)

        submitted = st.form_submit_button("Save details")
        if submitted:
            st.session_state["draft_inputs"] = {
                "doc_type": doc_type,
                "sender": sender,
                "sender_addr": sender_addr,
                "sender_email": sender_email,
                "recipient": recipient,
                "recipient_addr": recipient_addr,
                "subject": subject,
                "tone": tone,
                "relationship": relationship,
                "issue": issue,
                "amount": amount,
                "deadline": deadline,
                "demand": demand,
                "evidence": evidence,
                "governing": governing,
                "opt_without_prejudice": opt_without_prejudice,
                "opt_payment_plan": opt_payment_plan,
                "opt_preserve_evidence": opt_preserve_evidence,
            }
            st.success("Saved. You can generate the draft below.")

    st.write("")

    if "draft_inputs" in st.session_state and st.session_state["draft_inputs"].get("doc_type") == "Demand / Notice Letter":
        c3, c4 = st.columns([1, 1])
        with c3:
            gen = st.button("Generate draft", type="primary")
        with c4:
            if st.button("Reset saved details"):
                st.session_state.pop("draft_inputs", None)
                st.session_state.pop("draft_preview_md", None)
                st.rerun()

        if gen:
            draft_md = render_notice_letter(st.session_state["draft_inputs"], jurisdiction)
            st.session_state["draft_preview_md"] = draft_md

        draft_md = st.session_state.get("draft_preview_md", "")

# -------- Other (custom) --------
elif doc_type == "Other (custom)":
    st.subheader("Custom document (AI-assisted)")

    st.markdown(
        "<span style='color: rgba(2,6,23,0.65);'>"
        "Provide structured details. LegalEase will generate a conservative draft with placeholders for missing info."
        "</span>",
        unsafe_allow_html=True
    )

    with st.form("custom_form"):
        title = st.text_input("Document title", placeholder="e.g., Partnership Agreement / MoU / Settlement Agreement")
        doc_kind = st.text_input("Document category/type", placeholder="e.g., MoU, Agreement, Notice, Policy")

        parties = st.text_area(
            "Parties (who is involved?)",
            placeholder="e.g., Party A: ABC Pvt Ltd (Client)\nParty B: John Doe (Consultant)",
            height=90,
        )

        goal = st.text_area(
            "Goal (what should this document achieve?)",
            placeholder="e.g., Define responsibilities, payment terms, IP ownership, and termination.",
            height=80,
        )

        facts = st.text_area(
            "Key facts / situation (facts only)",
            placeholder="e.g., Contractor will build an app in 6 weeks; client provides content; milestone reviews weekly.",
            height=110,
        )

        terms = st.text_area(
            "Key terms (money/timeline/constraints)",
            placeholder="e.g., ₹50,000 total; 50% upfront; deliver by April 15; two revisions included.",
            height=90,
        )

        tone = st.selectbox("Tone", ["Neutral", "Friendly", "Firm"], index=0)

        clauses = st.multiselect(
            "Clauses to include (select as needed)",
            [
                "Confidentiality",
                "IP ownership",
                "Payment terms",
                "Milestones & acceptance",
                "Termination",
                "Limitation of liability",
                "Indemnity",
                "Non-solicitation",
                "Non-compete (jurisdiction-sensitive)",
                "Dispute resolution",
                "Governing law",
            ],
            default=["Payment terms", "Termination", "Dispute resolution", "Governing law"],
        )

        signatures = st.checkbox("Include signature blocks", value=True)

        extra = st.text_area(
            "Extra instructions (optional)",
            placeholder="e.g., Keep it 1–2 pages. Add an Exhibit A for deliverables.",
            height=80,
        )

        st.write("")
        safety_ack = st.checkbox("I understand this is informational drafting help, not legal advice.", value=False)

        submitted = st.form_submit_button("Save details")
        if submitted:
            if not safety_ack:
                st.warning("Please acknowledge the informational-only disclaimer to proceed.")
            else:
                st.session_state["draft_inputs"] = {
                    "doc_type": doc_type,
                    "title": title,
                    "doc_kind": doc_kind,
                    "parties": parties,
                    "goal": goal,
                    "facts": facts,
                    "terms": terms,
                    "tone": tone,
                    "clauses": clauses,
                    "signatures": "Yes" if signatures else "No",
                    "extra": extra,
                }
                st.success("Saved. You can generate the draft below.")

    st.write("")

    if "draft_inputs" in st.session_state and st.session_state["draft_inputs"].get("doc_type") == "Other (custom)":
        c3, c4 = st.columns([1, 1])
        with c3:
            gen = st.button("Generate draft", type="primary")
        with c4:
            if st.button("Reset saved details"):
                st.session_state.pop("draft_inputs", None)
                st.session_state.pop("draft_preview_md", None)
                st.rerun()

        if gen:
            with st.spinner("Generating…"):
                draft_md = draft_custom_markdown(st.session_state["draft_inputs"], jurisdiction)
            st.session_state["draft_preview_md"] = draft_md

        draft_md = st.session_state.get("draft_preview_md", "")



# ---------------- Preview + AI Polish ----------------
if draft_md:
    st.subheader("Draft preview")

    c5, c6 = st.columns([1, 1])
    with c5:
        ai_polish = st.button("AI Polish (improve wording)")
    with c6:
        st.caption("Keeps facts same; improves clarity.")

    if ai_polish:
        with st.spinner("Polishing…"):
            polished = polish_markdown(draft_md, jurisdiction)
        st.session_state["draft_preview_md"] = polished
        draft_md = polished
        st.success("Polished draft ready.")

    st.text_area("Generated draft (Markdown)", value=draft_md, height=520)

    st.download_button(
        "Download as .md",
        data=draft_md.encode("utf-8"),
        file_name="LegalEase_Draft.md",
        mime="text/markdown",
    )

