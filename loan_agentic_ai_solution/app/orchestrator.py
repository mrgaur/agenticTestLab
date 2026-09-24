from datetime import datetime, timezone
from langgraph.graph import StateGraph, END
from app.state import LoanState
from app.models import LoanApplication, LoanDecisionResponse, Decision
from app.agents.profile_agent import run_profile_agent
from app.agents.risk_agent import run_risk_agent
from app.agents.decision_agent import run_decision_agent
from app.agents.action_agent import run_action_agent
from app.llm_explainer import explain_with_llm
from app.policy import POLICY_VERSION
from app.repository import decision_repository

def finalize(state: LoanState) -> dict:
    decision = state["decision_result"].data
    action = state["action_result"].data
    factors = decision["key_decision_factors"]
    response = LoanDecisionResponse(
        case_id=action["case_id"], applicant_id=state["application"].applicant_id,
        decision=Decision(decision["classification"]), risk_score=decision["risk_score"],
        confidence=decision["confidence"], key_factors=factors,
        explanation=explain_with_llm(decision["classification"], factors, state["risk_result"].data),
        action_taken=action["action_taken"], notification_sent=action["notification_sent"],
        policy_version=POLICY_VERSION,
        agent_results=[state["profile_result"], state["risk_result"], state["decision_result"], state["action_result"]],
        audit_trail=state["audit_trail"], decided_at=datetime.now(timezone.utc),
    )
    decision_repository.save(response)
    return {"final_response": response}

def build_graph():
    graph = StateGraph(LoanState)
    graph.add_node("profile", run_profile_agent)
    graph.add_node("risk", run_risk_agent)
    graph.add_node("decision", run_decision_agent)
    graph.add_node("action", run_action_agent)
    graph.add_node("finalize", finalize)
    graph.set_entry_point("profile")
    graph.add_edge("profile", "risk")
    graph.add_edge("risk", "decision")
    graph.add_edge("decision", "action")
    graph.add_edge("action", "finalize")
    graph.add_edge("finalize", END)
    return graph.compile()

workflow = build_graph()

def evaluate_application(application: LoanApplication) -> LoanDecisionResponse:
    result = workflow.invoke({"application": application, "audit_trail": []})
    return result["final_response"]
