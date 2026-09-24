"""Reference FastMCP server exposing deterministic domain tools."""
from mcp.server.fastmcp import FastMCP
from app.models import LoanApplication
from app.agents.profile_agent import run_profile_agent
from app.agents.risk_agent import run_risk_agent

mcp = FastMCP("loan-domain-tools")

@mcp.tool()
def analyze_applicant_profile(application: dict) -> dict:
    app = LoanApplication.model_validate(application)
    return run_profile_agent({"application": app, "audit_trail": []})["profile_result"].model_dump(mode="json")

@mcp.tool()
def analyze_financial_risk(application: dict) -> dict:
    app = LoanApplication.model_validate(application)
    return run_risk_agent({"application": app, "audit_trail": []})["risk_result"].model_dump(mode="json")

if __name__ == "__main__":
    mcp.run()
