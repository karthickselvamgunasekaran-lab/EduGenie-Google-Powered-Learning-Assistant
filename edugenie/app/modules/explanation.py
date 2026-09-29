from app.ai.gemini import gemini_service
from app.ai.prompts import EXPLANATION


def explain_topic(topic: str) -> str:
    if gemini_service.available:
        return gemini_service.generate(EXPLANATION.format(topic=topic))

    return (
        f"{topic.title()} is a concept that can be learned step by step. "
        f"Start with its definition, understand the main ideas, and then practice "
        f"with a simple example. Demo mode is active; add GEMINI_API_KEY for a "
        f"topic-specific AI explanation."
    )
