# Agentic AI Loan Approval System

A simple college project demonstrating a loan-application workflow using **Python, Streamlit, and Anthropic Claude**.

## Features
- Streamlit form for loan data
- Claude-based decision-synthesis agent
- Explainable recommendation, risk score, confidence, factors, and compliance note
- Downloadable JSON audit record

## Safety note
This is an educational prototype, not a production underwriting system. A qualified human must review every result, and protected characteristics must not be used.

## Architecture
1. Presentation layer: Streamlit form
2. Orchestration layer: `app.py` creates the application payload and prompt
3. AI decision agent: Claude returns structured JSON
4. Audit layer: JSON download

## Run it
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
streamlit run app.py
```

For PowerShell, use `$env:ANTHROPIC_API_KEY="your_key_here"`.

## Extension ideas
- Split profile, risk, compliance, and decision checks into LangGraph nodes.
- Add FastAPI endpoints and a database.
- Add validation rules and automated tests.
