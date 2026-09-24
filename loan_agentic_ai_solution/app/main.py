from fastapi import FastAPI, HTTPException
from app.models import LoanApplication, LoanDecisionResponse
from app.orchestrator import evaluate_application
from app.repository import decision_repository

app = FastAPI(title="Agentic AI Loan Approval API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/loan-applications", response_model=LoanDecisionResponse)
def submit_application(application: LoanApplication):
    return evaluate_application(application)

@app.get("/v1/loan-applications/{case_id}", response_model=LoanDecisionResponse)
def get_application(case_id: str):
    result = decision_repository.get(case_id)
    if not result:
        raise HTTPException(status_code=404, detail="Case not found")
    return result
