from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, model_validator

class EmploymentType(str, Enum):
    SALARIED = "SALARIED"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    CONTRACT = "CONTRACT"
    UNEMPLOYED = "UNEMPLOYED"

class Decision(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    MANUAL_REVIEW = "MANUAL_REVIEW"

class LoanApplication(BaseModel):
    applicant_id: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=18, le=120, description="Collected input; excluded from scoring")
    annual_income: float = Field(gt=0)
    employment_type: EmploymentType
    employment_months: int = Field(ge=0)
    credit_score: int = Field(ge=300, le=900)
    loan_amount: float = Field(gt=0)
    tenure_months: int = Field(gt=0, le=480)
    monthly_liabilities: float = Field(ge=0)
    location: str = Field(min_length=1, max_length=200, description="Collected input; excluded from scoring")
    application_timestamp: datetime

    @model_validator(mode="after")
    def timestamp_has_timezone(self):
        if self.application_timestamp.tzinfo is None:
            raise ValueError("application_timestamp must include timezone information")
        return self

class AgentResult(BaseModel):
    agent: str
    status: str = "SUCCESS"
    data: dict[str, Any]
    reasons: list[str] = []

class AuditEvent(BaseModel):
    timestamp: datetime
    component: str
    action: str
    details: dict[str, Any] = {}

class LoanDecisionResponse(BaseModel):
    case_id: str
    applicant_id: str
    decision: Decision
    risk_score: int = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    key_factors: list[str]
    explanation: str
    action_taken: str
    notification_sent: bool
    policy_version: str
    agent_results: list[AgentResult]
    audit_trail: list[AuditEvent]
    decided_at: datetime
