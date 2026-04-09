# PitchIQ

Autonomous multi-agent system that researches hotel prospects and generates personalized outreach at scale.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-green?style=flat-square)
![LangGraph](https://img.shields.io/badge/LangGraph-1.1-orange?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-purple?style=flat-square)
![React](https://img.shields.io/badge/React-18-cyan?style=flat-square&logo=react)

## Background

Cold outreach fails because it's generic. PitchIQ fixes that by researching a prospect in real-time, qualifying the lead, and writing outreach based on what's actually happening at their property — before you've sent a single message.

## Requirements

- Python 3.11+
- PostgreSQL 16+
- gcloud CLI
- Node.js 18+ (frontend only)

## Install

    git clone https://github.com/Jayasurya29/pitchiq.git
    cd pitchiq
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

Contact a contributor for required environment variables.

    gcloud auth application-default login
    python -m uvicorn api.main:app --reload

## Usage

API docs at http://localhost:8000/docs

Submit a contact via `POST /research`. Review generated outreach at `GET /pending`. Approve with `POST /approve/{id}`.

## Stack

- LangGraph + Gemini 2.5 Flash (Vertex AI)
- FastAPI + PostgreSQL
- React + TypeScript (in progress)

## Contributing

Open an issue or submit a PR against `main`. Work from feature branches — see `commands.txt` for the git workflow.

## Contributors

[@Jayasurya29](https://github.com/Jayasurya29) · [@eternal888](https://github.com/eternal888)

## License

MIT
