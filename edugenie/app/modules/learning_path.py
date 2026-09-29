from app.ai.gemini import gemini_service
from app.ai.prompts import LEARNING


def get_learning_recommendations(topic: str) -> str:
    if gemini_service.available:
        return gemini_service.generate(LEARNING.format(topic=topic))

    return (
        f"Learning path for {topic} (demo mode)\n\n"
        "Beginner: learn terminology, core concepts, and one small hands-on exercise.\n"
        "Intermediate: study how the major concepts work together and complete several exercises.\n"
        "Advanced: build a small project, review trade-offs, and solve progressively harder problems.\n\n"
        "Configure GEMINI_API_KEY for a personalized AI-generated path."
    )
