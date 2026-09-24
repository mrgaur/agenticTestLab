import json
from app.config import settings

def deterministic_explanation(decision: str, factors: list[str]) -> str:
    return f"Decision: {decision}. Factors: " + "; ".join(factors) + ". The decision was produced by versioned deterministic demo rules."

def explain_with_llm(decision: str, factors: list[str], metrics: dict) -> str:
    if not settings.anthropic_api_key:
        return deterministic_explanation(decision, factors)
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=settings.anthropic_api_key)
        prompt = {
            "decision": decision,
            "factors": factors,
            "metrics": metrics,
            "instruction": "Explain only these supplied facts in concise, neutral language. Do not add facts, change the decision, or mention protected attributes."
        }
        response = client.messages.create(
            model=settings.anthropic_model,
            max_tokens=250,
            messages=[{"role": "user", "content": json.dumps(prompt)}],
        )
        text = "".join(block.text for block in response.content if getattr(block, "type", "") == "text").strip()
        return text or deterministic_explanation(decision, factors)
    except Exception:
        return deterministic_explanation(decision, factors)
