from datetime import datetime, timezone
from app.models import LoanApplication, Decision
from app.orchestrator import evaluate_application

def application(**overrides):
    data = dict(applicant_id="T-1", age=35, annual_income=1200000, employment_type="SALARIED",
                employment_months=72, credit_score=760, loan_amount=2000000, tenure_months=120,
                monthly_liabilities=18000, location="Mumbai", application_timestamp=datetime.now(timezone.utc))
    data.update(overrides)
    return LoanApplication(**data)

def test_approve_low_risk():
    assert evaluate_application(application()).decision == Decision.APPROVED

def test_reject_low_credit():
    assert evaluate_application(application(credit_score=520)).decision == Decision.REJECTED

def test_review_borderline_credit():
    assert evaluate_application(application(credit_score=650)).decision == Decision.MANUAL_REVIEW

def test_age_and_location_do_not_change_score():
    a = evaluate_application(application(age=25, location="A"))
    b = evaluate_application(application(age=70, location="B"))
    assert a.risk_score == b.risk_score
