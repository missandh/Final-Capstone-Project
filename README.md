# Practo Domain Agent

A Python-based clinical decision-support and governance prototype for a domain-specific assistant that retrieves policy context, evaluates escalation risk, and enforces guardrails before returning a response.

## Project goals

- Generate synthetic appointment and clinical data.
- Build a small retrieval-augmented generation (RAG) pipeline.
- Apply policy retrieval and citation-aware evaluation.
- Enforce guardrails for PII handling and prompt injection.
- Provide a FastAPI API and a structured tracing layer.
- Add review and governance layers for controlled autonomy.

## Repository structure

- `data/`: synthetic datasets and policy knowledge base
- `rag/`: indexing, chunking, retrieval, and evaluation utilities
- `core/`: LLM abstractions, schemas, guardrails, memory, cache, and configuration
- `agents/`: multi-agent orchestration and review agents
- `governance/`: runtime autonomy and token budget controls
- `evaluation/`: benchmark-style evaluation harness
- `api/`: HTTP and WebSocket application endpoints
- `scripts/`: one-click validation and transcript generation

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python scripts/run_all_checks.py
```

## Environment configuration

The project reads settings from environment variables and a local `.env` file. Sample values are provided in `.env.example`.

Example:

```bash
APP_NAME="Practo Domain Agent"
APP_ENV="development"
MAX_TOKENS=500
MAX_AUTONOMY=2
API_PREFIX="/api/v1"
```

## Running the API

```bash
uvicorn api.app:app --reload
```

Then open:

- `http://localhost:8000/health`
- `http://localhost:8000/docs`

## Tests

```bash
pytest -q
```

## License

This project is intended for educational and prototype use.
