import os
from datetime import datetime
import httpx
import streamlit as st

API = os.getenv("API_BASE_URL", "http://localhost:8000")
st.set_page_config(page_title="Loan Approval Agentic AI", layout="wide")
st.title("Agentic AI Intelligent Loan Approval")
st.caption("Educational reference. Final decisions in real lending require approved governance and human oversight.")

with st.form("loan"):
    c1, c2 = st.columns(2)
    with c1:
        applicant_id = st.text_input("Applicant ID", "APP-1001")
        age = st.number_input("Age", 18, 120, 35)
        annual_income = st.number_input("Annual income", min_value=1.0, value=1200000.0)
        employment_type = st.selectbox("Employment type", ["SALARIED", "SELF_EMPLOYED", "CONTRACT", "UNEMPLOYED"])
        employment_months = st.number_input("Employment months", min_value=0, value=72)
    with c2:
        credit_score = st.number_input("Credit score", 300, 900, 760)
        loan_amount = st.number_input("Loan amount", min_value=1.0, value=2000000.0)
        tenure_months = st.number_input("Tenure months", 1, 480, 120)
        monthly_liabilities = st.number_input("Monthly liabilities", min_value=0.0, value=18000.0)
        location = st.text_input("Location", "Mumbai")
    submitted = st.form_submit_button("Evaluate")

if submitted:
    payload = {"applicant_id": applicant_id, "age": age, "annual_income": annual_income,
               "employment_type": employment_type, "employment_months": employment_months,
               "credit_score": credit_score, "loan_amount": loan_amount, "tenure_months": tenure_months,
               "monthly_liabilities": monthly_liabilities, "location": location,
               "application_timestamp": datetime.now().astimezone().isoformat()}
    try:
        response = httpx.post(f"{API}/v1/loan-applications", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        st.subheader(data["decision"])
        st.metric("Risk score", data["risk_score"])
        st.write(data["explanation"])
        with st.expander("Decision factors"):
            st.write(data["key_factors"])
        with st.expander("Agent results and audit trail"):
            st.json(data)
    except Exception as exc:
        st.error(f"Request failed: {exc}")
