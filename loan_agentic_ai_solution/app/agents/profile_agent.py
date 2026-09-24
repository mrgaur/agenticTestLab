from datetime import datetime, timezone
from app.models import AgentResult, AuditEvent
from app.state import LoanState

def run_profile_agent(state: LoanState) -> dict:
    app = state["application"]
    flags = []
    if app.employment_months < 12:
        flags.append("Limited employment history")
    if app.employment_type.value == "UNEMPLOYED":
        flags.append("No current employment")
    stability = max(0, min(100, int(app.employment_months / 60 * 100)))
    result = AgentResult(
        agent="ApplicantProfileAgent",
        data={
            "income_stability_score": stability,
            "employment_risk": "HIGH" if flags else "LOW",
            "credit_history_summary": f"Declared credit score: {app.credit_score}",
            "application_completeness_flags": [],
            "profile_flags": flags,
            "excluded_from_scoring": ["age", "location"],
        },
        reasons=flags or ["Profile validation completed"],
    )
    event = AuditEvent(timestamp=datetime.now(timezone.utc), component=result.agent, action="PROFILE_CHECK", details=result.data)
    return {"profile_result": result, "audit_trail": state.get("audit_trail", []) + [event]}
