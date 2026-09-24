from datetime import datetime, timezone
from uuid import uuid4
from app.models import AgentResult, AuditEvent
from app.state import LoanState

def run_action_agent(state: LoanState) -> dict:
    decision = state["decision_result"].data["classification"]
    case_id = f"LOAN-{uuid4().hex[:12].upper()}"
    action = {"APPROVED": "Record approval and initiate downstream processing", "REJECTED": "Record rejection and prepare governed reason notice", "MANUAL_REVIEW": "Create human-review task"}[decision]
    data = {"action_taken": action, "notification_sent": False, "case_id": case_id, "timestamp": datetime.now(timezone.utc).isoformat(), "summary": f"{decision} decision recorded"}
    result = AgentResult(agent="ComplianceActionOrchestratorAgent", data=data, reasons=["Action derived from deterministic decision"])
    event = AuditEvent(timestamp=datetime.now(timezone.utc), component=result.agent, action="ACTION_RECORDED", details=data)
    return {"action_result": result, "audit_trail": state.get("audit_trail", []) + [event]}
