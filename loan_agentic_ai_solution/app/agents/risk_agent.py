from datetime import datetime, timezone
from app.models import AgentResult, AuditEvent
from app.state import LoanState
from app import policy

def run_risk_agent(state: LoanState) -> dict:
    app = state["application"]
    monthly_income = app.annual_income / 12
    dti = app.monthly_liabilities / monthly_income
    loan_income_ratio = app.loan_amount / app.annual_income
    hits, score = [], 0
    if app.credit_score < policy.MIN_CREDIT_SCORE:
        hits.append("Credit score below minimum policy threshold"); score += 55
    elif app.credit_score < policy.REVIEW_CREDIT_SCORE:
        hits.append("Credit score in manual-review band"); score += 25
    if dti > policy.MAX_DTI_REJECT:
        hits.append("Debt-to-income ratio above rejection threshold"); score += 50
    elif dti > policy.MAX_DTI_REVIEW:
        hits.append("Debt-to-income ratio in manual-review band"); score += 25
    if loan_income_ratio > policy.MAX_LOAN_TO_ANNUAL_INCOME_REVIEW:
        hits.append("Loan amount high relative to annual income"); score += 20
    if app.employment_months < policy.MIN_EMPLOYMENT_MONTHS_REVIEW:
        hits.append("Employment history below review threshold"); score += 15
    if app.employment_type.value == "UNEMPLOYED":
        hits.append("Applicant has no current employment"); score += 40
    score = min(100, score)
    data = {
        "debt_to_income_ratio": round(dti, 4),
        "credit_score_risk_level": "HIGH" if app.credit_score < 580 else "MEDIUM" if app.credit_score < 680 else "LOW",
        "loan_to_annual_income_ratio": round(loan_income_ratio, 4),
        "anomaly_flags": [],
        "rule_hits": hits,
        "risk_score": score,
    }
    result = AgentResult(agent="FinancialRiskAnalysisAgent", data=data, reasons=hits or ["No elevated risk rule triggered"])
    event = AuditEvent(timestamp=datetime.now(timezone.utc), component=result.agent, action="RISK_ANALYSIS", details=data)
    return {"risk_result": result, "audit_trail": state.get("audit_trail", []) + [event]}
