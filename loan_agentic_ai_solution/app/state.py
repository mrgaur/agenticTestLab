from typing import TypedDict
from app.models import LoanApplication, AgentResult, AuditEvent, LoanDecisionResponse

class LoanState(TypedDict, total=False):
    application: LoanApplication
    profile_result: AgentResult
    risk_result: AgentResult
    decision_result: AgentResult
    action_result: AgentResult
    audit_trail: list[AuditEvent]
    final_response: LoanDecisionResponse
