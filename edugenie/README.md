# EduGenie — AI Learning Assistant

EduGenie is a full-stack learning-support application based on the supplied project documentation. It provides:

- Q&A
- Simple topic explanations
- Paragraph summarization
- AI-generated multiple-choice quizzes
- Adaptive learning recommendations
- A browser-based frontend
- FastAPI backend
- Gemini integration with a safe demo fallback when no API key is configured
- Automated API tests
- Docker support

The reference documentation describes the EduGenie flow as a frontend that sends the user's selection to FastAPI, which routes to explanation, Q&A, quiz, summarization, or learning-recommendation modules and then displays the result.

## 1. Requirements

- Python 3.11+
- VS Code
- Optional: a Google Gemini API key for live AI responses
- Optional: Docker Desktop

## 2. VS Code setup

1. Open the `edugenie` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Copy the environment template:

```bash
cp .env.example .env
```

On Windows, copy `.env.example` to `.env` manually if `cp` is unavailable.

6. Put your Gemini API key in `.env`:

```env
GEMINI_API_KEY=your_key_here
```

The app also runs without a key in `DEMO_MODE`, so the UI and API can be tested locally without external AI access.

## 3. Run the application

```bash
uvicorn app.main:app --reload
```

Open:

- Frontend: http://127.0.0.1:8000/
- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/api/health

## 4. Run tests

```bash
pytest -q
```

## 5. Docker

```bash
docker compose up --build
```

Then open http://127.0.0.1:8000/.

## 6. API examples

### Q&A

```bash
curl "http://127.0.0.1:8000/api/qna?question=Why%20is%20the%20sky%20blue?"
```

### Explanation

```bash
curl -X POST "http://127.0.0.1:8000/api/explain" \
  -H "Content-Type: application/json" \
  -d '{"topic":"photosynthesis"}'
```

### Summarization

```bash
curl -X POST "http://127.0.0.1:8000/api/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text":"Photosynthesis is the process by which plants convert light energy into chemical energy."}'
```

### Quiz

```bash
curl -X POST "http://127.0.0.1:8000/api/quiz" \
  -H "Content-Type: application/json" \
  -d '{"text":"The Pythagorean theorem relates the sides of a right triangle."}'
```

### Learning recommendations

```bash
curl "http://127.0.0.1:8000/api/learn/recommendations?topic=SQL"
```

## 7. Project structure

```text
edugenie/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── gemini.py
│   │   └── prompts.py
│   └── modules/
│       ├── __init__.py
│       ├── qna.py
│       ├── explanation.py
│       ├── summary.py
│       ├── quiz.py
│       └── learning_path.py
├── static/
│   ├── index.html
│   ├── app.js
│   └── style.css
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 8. Troubleshooting

### `ModuleNotFoundError`

Make sure the virtual environment is active and run:

```bash
pip install -r requirements.txt
```

### Port 8000 is already in use

```bash
uvicorn app.main:app --reload --port 8001
```

Then open http://127.0.0.1:8001/.

### Gemini is unavailable

The application automatically uses demo responses when `GEMINI_API_KEY` is missing or when `AI_PROVIDER=demo`.

For live Gemini responses, set:

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

If your Google account exposes a different current Gemini model, change `GEMINI_MODEL` without changing application code.

## 9. Production notes

For production, put the API behind HTTPS, restrict CORS to the real frontend origin, add authentication/rate limiting, and store secrets in a secret manager rather than committing `.env`.
