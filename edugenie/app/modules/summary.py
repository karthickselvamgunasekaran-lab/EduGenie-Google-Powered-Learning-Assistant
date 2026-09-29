import re

from app.ai.gemini import gemini_service
from app.ai.prompts import SUMMARY


def _demo_summary(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s for s in sentences if s]
    if not sentences:
        return "No text was provided."
    chosen = sentences[:3]
    return " ".join(chosen) + (
        "\n\nDemo mode is active; add GEMINI_API_KEY for an AI-generated summary."
    )


def summarize_text(text: str) -> str:
    if gemini_service.available:
        return gemini_service.generate(SUMMARY.format(text=text))
    return _demo_summary(text)
