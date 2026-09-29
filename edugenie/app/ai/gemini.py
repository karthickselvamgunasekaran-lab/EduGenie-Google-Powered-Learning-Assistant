import json
import re
from typing import Any

try:
    from google import genai
except ImportError:  # Allows demo mode and tests before optional AI dependencies are installed.
    genai = None

from app.config import get_settings
from app.ai.prompts import SYSTEM


class GeminiService:
    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self._client: Any | None = None

    @property
    def available(self) -> bool:
        return not self.settings.demo_mode

    def _client_or_create(self):
        if genai is None:
            raise RuntimeError("google-genai is not installed. Run: pip install -r requirements.txt")
        if self._client is None:
            self._client = genai.Client(api_key=self.settings.gemini_api_key)
        return self._client

    def generate(self, prompt: str) -> str:
        if not self.available:
            raise RuntimeError("Gemini is not configured; using demo mode.")
        client = self._client_or_create()
        response = client.models.generate_content(
            model=self.settings.gemini_model,
            contents=f"{SYSTEM}\n\n{prompt}",
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()

    @staticmethod
    def extract_json(text: str) -> Any:
        cleaned = text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        start = min(
            [i for i in (cleaned.find("["), cleaned.find("{")) if i >= 0],
            default=-1,
        )
        if start < 0:
            raise ValueError("No JSON object or array found in model response.")

        for end in range(len(cleaned), start, -1):
            candidate = cleaned[start:end]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue

        raise ValueError("Model response did not contain valid JSON.")


gemini_service = GeminiService()
