# Agentic AI Intelligent Loan Approval System

A runnable reference implementation based on the supplied case study. It uses FastAPI, LangGraph, Streamlit, auditable state transitions, domain agents, deterministic policy guardrails, and an optional Anthropic explanation layer.

> Important: This is an educational reference implementation, not a production lending policy. Age and location are accepted because they appear in the case-study input, but are **not used for approval scoring**. Legal, compliance, model-risk, fairness, security, and human-review controls must be approved before real use.

## Architecture

```text
Streamlit UI -> FastAPI API -> LangGraph Orchestrator
                                  |-> Applicant Profile Agent
                                  |-> Financial Risk Agent
                                  |-> Decision Agent
                                  |-> Compliance and Action Agent
Optional explanation: Anthropic Claude (facts constrained by deterministic results)
Persistence: in-memory demo repository; replace with approved systems
```

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

In another terminal:

```bash
streamlit run ui/streamlit_app.py
```

Open API docs at `http://localhost:8000/docs`.

## Sample request

```bash
curl -X POST http://localhost:8000/v1/loan-applications \
  -H "Content-Type: application/json" \
  -d @sample_application.json
```

## Decision policy in this reference

- Hard policy failure: REJECTED.
- Otherwise high risk, missing required data, or borderline threshold: MANUAL_REVIEW.
- Otherwise: APPROVED.
- The LLM may explain a decision but cannot change it.
- Every response includes rule hits, agent outputs, confidence, case ID, and audit events.

## MCP

`mcp_servers/tools_server.py` exposes reference tools through FastMCP when the installed MCP package supports it. The primary local runtime calls the same domain services directly, so the demo remains easy to run and test. In production, deploy MCP servers independently and add authentication, authorization, mTLS, schema/version governance, timeouts, retries, and observability.

## Tests

```bash
pytest -q
```

## Production hardening checklist

1. Replace mock/in-memory repositories with approved applicant, risk-rule, case-management, and notification systems.
2. Externalize policy rules with versioning, maker-checker approval, effective dates, rollback, and immutable audit history.
3. Add OAuth2/OIDC, RBAC/ABAC, secrets vault, encryption, tokenization, retention, consent, and field-level access control.
4. Add fairness testing, adverse-action reason governance, drift monitoring, threshold validation, and independent model-risk review.
5. Add queues, idempotency keys, circuit breakers, retries, distributed tracing, metrics, structured logs, and dead-letter handling.
6. Keep final approval authority deterministic and policy-controlled; require human approval for review cases.
