# SmartAssist — AI-Powered Website Chatbot

A responsive customer-support chatbot built with **Python, Flask, HTML, CSS, and JavaScript**. It uses explainable retrieval-based intent matching and approved sample answers, with a fallback when confidence is low. No paid AI API key is required.

> **Demo status:** This is a locally runnable project with deployment instructions. It is not automatically deployed to AWS. Replace sample hours, pricing, support, and policy replies with verified information before public use.

## Features
- Responsive landing page and floating chat widget
- Predefined intent patterns and retrieval-based matching
- Confidence threshold and safe fallback
- Suggested questions, typing indicator, and timestamps
- Flask JSON API, validation, request size limits, health endpoint
- Automated unit/API tests
- Dockerfile and Docker Compose
- AWS deployment guide
- No server-side conversation history by default

## Stack
Python 3.10+, Flask, Waitress, HTML5, CSS, vanilla JavaScript, JSON, unittest, Docker.

## Structure
```text
smartassist-ai-chatbot/
├── app.py
├── chatbot.py
├── intents.json
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── templates/index.html
├── static/css/style.css
├── static/js/chatbot.js
├── tests/test_chatbot.py
└── docs/
    ├── ARCHITECTURE.md
    ├── DEPLOYMENT.md
    ├── TEST-REPORT.md
    └── SUBMISSION-CHECKLIST.md
```

## Run locally
1. Install Python 3.10 or newer.
2. From this folder, create a virtual environment:
   - Windows PowerShell: `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
3. Install dependencies: `python -m pip install -r requirements.txt`
4. Start: `python app.py`
5. Open `http://127.0.0.1:5000`.

If PowerShell blocks activation, run `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\python.exe app.py`.

## Tests
Run from the project root:
```bash
python -m unittest discover -s tests -v
```
Record the actual test result in `docs/TEST-REPORT.md`. These tests do not replace security, accessibility, load, or user-acceptance testing.

## Docker
```bash
docker compose up --build
```
Open `http://localhost:8080`. Stop with `Ctrl+C`; clean up with `docker compose down`.

## API
- `GET /health` — service health
- `GET /api/intents` — suggested visitor questions (does not expose training patterns)
- `POST /api/chat` — JSON body `{"message":"hello"}`

Successful response example:
```json
{"reply":"Hello! Welcome to SmartAssist. How can I help you today?","intent":"greeting","confidence":1.0,"matched":true}
```
The `confidence` score is a heuristic, not a calibrated probability. Messages must be non-empty and no longer than 1,000 characters.

## Customize training patterns
Edit `intents.json`. Each intent includes a `tag`, `patterns`, and `responses`. Add natural paraphrases, avoid overlapping patterns, and evaluate with a held-out test set that was not used for training. Replace every sample business statement with verified, current information.

Environment variables:
- `PORT` — port for local app (default `5000`; Docker defaults to `8080`)
- `INTENTS_PATH` — optional alternate intents JSON file
- `CONFIDENCE_THRESHOLD` — match cutoff (default `0.52`)

## Limitations and production readiness
This project is an intent-matching demo, not an LLM or semantic search system. It can miss paraphrases, misspellings, multilingual input, or questions outside the dataset. The score is not a probability. Before commercial use, add representative evaluation, rate limiting, TLS, abuse controls, reviewed knowledge, operational monitoring, privacy/retention controls, and live-agent handoff as appropriate.

## AWS
See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md). Options include Elastic Beanstalk or a container deployment on ECS Fargate behind an HTTPS load balancer, with CloudWatch logs/metrics. **This repository does not create AWS resources or mean the app is deployed.** Review regional prices and set a budget before provisioning resources.

## Docs
- [Architecture](docs/ARCHITECTURE.md)
- [Deployment guide](docs/DEPLOYMENT.md)
- [Test report](docs/TEST-REPORT.md)
- [Submission checklist](docs/SUBMISSION-CHECKLIST.md)

## Security
Never commit API keys, passwords, `.env` files, or private customer data. Flask debug mode is disabled. Use HTTPS, least-privilege IAM, rate limits, monitoring, and secure secret storage for public deployments. If adding a generative AI API, keep the API key on the server, never in browser JavaScript.

## License
MIT — see `LICENSE`.
