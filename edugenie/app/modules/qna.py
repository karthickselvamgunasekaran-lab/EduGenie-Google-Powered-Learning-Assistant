from app.ai.gemini import gemini_service
from app.ai.prompts import QNA


def answer_question(question: str) -> str:
    if gemini_service.available:
        return gemini_service.generate(QNA.format(question=question))

    return (
        f"Demo mode: Your question is “{question}”. "
        "Configure GEMINI_API_KEY in .env to receive a live AI-generated answer."
    )
