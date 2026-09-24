import json
import os
from datetime import datetime

import anthropic
import streamlit as st

st.set_page_config(page_title="Loan Approval Assistant")
st.title("Agentic AI Loan Approval System")
st.caption("College project demo — decisions require a qualified loan officer's review.")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Anthropic API key", type="password", value=os.getenv("ANTHROPIC_API_KEY", ""))

with st.form("loan_application"):
    st.subheader("Loan application")
    applicant_id = st.text_input("Applicant ID", "APP-001")
    age = st.number_input("Age", 18, 100, 30)
    income = st.number_input("Annual income (USD)", min_value=0, value=65000)
    employment = st.selectbox("Employment type", ["Salaried", "Self-employed", "Contract", "Unemployed"])
    credit_score = st.number_input("Credit score", 300, 850, 720)
    loan_amount = st.number_input("Loan amount (USD)", min_value=1000, value=25000)
    tenure = st.number_input("Tenure (months)", 6, 360, 36)
    liabilities = st.number_input("Monthly existing liabilities (USD)", min_value=0, value=500)
    location = st.text_input("Location", "New York")
    submitted = st.form_submit_button("Analyze application")

if submitted:
    application = {"applicant_id": applicant_id, "age": age, "annual_income": income, "employment_type": employment, "credit_score": credit_score, "loan_amount": loan_amount, "tenure_months": tenure, "monthly_liabilities": liabilities, "location": location, "application_timestamp": datetime.now().isoformat()}
    if not api_key:
        st.error("Enter an Anthropic API key to run the analysis.")
    else:
        prompt = """You are the decision-synthesis agent for a college demo loan workflow.
Return ONLY valid JSON with: decision (APPROVE, REJECT, or MANUAL_REVIEW), risk_score (0-100), confidence (LOW, MEDIUM, HIGH), factors (array of 3-5 strings), explanation, and compliance_note.
Calculate approximate debt-to-income as (monthly_liabilities * 12) / annual_income. Do not use protected characteristics, do not make a final real-world lending decision, and choose MANUAL_REVIEW when uncertain.

Application:
""" + json.dumps(application, indent=2)
        try:
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(model="claude-sonnet-4-6", max_tokens=700, temperature=0, messages=[{"role": "user", "content": prompt}])
            result = json.loads(response.content[0].text)
            st.subheader("Recommendation")
            st.metric("Decision", result.get("decision", "MANUAL_REVIEW"))
            left, right = st.columns(2)
            left.metric("Risk score", result.get("risk_score", "N/A"))
            right.metric("Confidence", result.get("confidence", "N/A"))
            st.write("**Key factors**")
            for factor in result.get("factors", []):
                st.write("- " + factor)
            st.info(result.get("explanation", "No explanation returned."))
            st.warning(result.get("compliance_note", "Human review is required."))
            st.download_button("Download audit record", json.dumps({"application": application, "analysis": result}, indent=2), "loan_audit_record.json")
        except Exception as exc:
            st.error("Analysis failed: " + str(exc))
