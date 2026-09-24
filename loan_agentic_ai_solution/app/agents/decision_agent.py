from datetime import datetime, timezone
from app.models import AgentResult, AuditEvent, Decision
from app.state import LoanState

def run_decision_agent(state: LoanState) -> dict:
    risk = state["risk_result"].data
    profile = state["profile_result"].data
    reasons = list(risk["rule_hits"]) + list(profile["profile_flags"])
    hard_reject = any(x in risk["rule_hits"] for x in [
        "Credit score below minimum policy threshold",
        "Debt-to-income ratio above rejection threshold",
    ]) or "No current employment" in profile["profile_flags"]
    review = risk["risk_score"] >= 20 or bool(profile["application_completeness_flags"])
    if hard_reject:
        decision, confidence = Decision.REJECTED, 0.95
    elif review:
        decision, confidence = Decision.MANUAL_REVIEW, 0.80
    else:
        decision, confidence = Decision.APPROVED, 0.90
    factors = reasons or ["Credit, affordability, and employment checks are within demo thresholds"]
    data = {"classification": decision.value, "risk_score": risk["risk_score"], "confidence": confidence, "key_decision_factors": factors}
    result = AgentResult(agent="LoanDecisionAgent", data=data, reasons=factors)
    event = AuditEvent(timestamp=datetime.now(timezone.utc), component=result.agent, action="DECISION_SYNTHESIS", details=data)
    return {"decision_result": result, "audit_trail": state.get("audit_trail", []) + [event]}
