from __future__ import annotations

import os

from dotenv import load_dotenv
from pydantic_ai import Agent


load_dotenv()

DEFAULT_MODEL = "openai:gpt-5-mini"
SHORT_INSTRUCTIONS = "Answer in one short sentence. Be direct and concise."


def _require_openai_key() -> None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "your_openai_api_key_here":
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add your OpenAI key to the .env file before running the app."
        )


_require_openai_key()

MODEL_NAME = os.getenv("MODEL_NAME", DEFAULT_MODEL).strip() or DEFAULT_MODEL

agent = Agent(
    MODEL_NAME,
    instructions=SHORT_INSTRUCTIONS,
)

