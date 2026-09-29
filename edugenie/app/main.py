from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.models import (
    AnswerResponse,
    ExplanationResponse,
    LearningResponse,
    QuizResponse,
    SummaryResponse,
    TextRequest,
    TopicRequest,
)
from app.modules.explanation import explain_topic
from app.modules.learning_path import get_learning_recommendations
from app.modules.qna import answer_question
from app.modules.quiz import generate_quiz
from app.modules.summary import summarize_text

settings = get_settings()
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="EduGenie AI learning assistant API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "ai_provider": settings.ai_provider,
        "demo_mode": settings.demo_mode,
    }


@app.get("/api/qna", response_model=AnswerResponse)
async def qna_api(question: str = Query(..., min_length=1, max_length=5000)):
    try:
        return {"answer": answer_question(question)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/api/explain", response_model=ExplanationResponse)
async def explain_api(request: TopicRequest):
    try:
        return {"topic": request.topic, "explanation": explain_topic(request.topic)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/api/summarize", response_model=SummaryResponse)
async def summarize_api(request: TextRequest):
    try:
        return {"summary": summarize_text(request.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/api/quiz", response_model=QuizResponse)
async def quiz_api(request: TextRequest):
    try:
        return {"quiz": generate_quiz(request.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/api/learn/recommendations", response_model=LearningResponse)
async def learning_recommendation_api(
    topic: str = Query(..., min_length=1, max_length=500)
):
    try:
        return {
            "topic": topic,
            "recommendation": get_learning_recommendations(topic),
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


# Compatibility routes matching the endpoint names shown in the reference project.
@app.get("/qna", include_in_schema=False)
async def legacy_qna(question: str = Query(..., min_length=1)):
    return await qna_api(question)


@app.post("/explain/", include_in_schema=False)
async def legacy_explain(request: TopicRequest):
    return await explain_api(request)


@app.post("/summarize/", include_in_schema=False)
async def legacy_summarize(request: TextRequest):
    return await summarize_api(request)


@app.post("/quiz", include_in_schema=False)
async def legacy_quiz(request: TextRequest):
    return await quiz_api(request)


@app.get("/learn/recommendations", include_in_schema=False)
async def legacy_learning(topic: str = Query(..., min_length=1)):
    return await learning_recommendation_api(topic)
