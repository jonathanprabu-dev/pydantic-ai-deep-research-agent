"""The shared model plus the small chat agent that answers briefly.

Which model runs is set by MODEL in .env, as "<provider>:<model name>":

    MODEL=google:gemini-3.6-flash
    MODEL=openrouter:nvidia/nemotron-3-super-120b-a12b:free

Only the first colon separates the provider, so OpenRouter's ":free" suffix
survives intact.
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from google.genai.types import HttpRetryOptions
from pydantic_ai import Agent
from pydantic_ai.models import Model
from pydantic_ai.models.concurrency import ConcurrencyLimitedModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.providers.openrouter import OpenRouterProvider

# Providers read their keys from the environment; .env is not loaded for us.
load_dotenv()

DEFAULT_MODEL = "google:gemini-3.6-flash"
# Which env var holds the key, per provider.
PROVIDER_KEYS = {"google": "GOOGLE_API_KEY", "openrouter": "OPENROUTER_API_KEY"}

# How many model requests one research run costs: planner + 4 analysts + synthesis.
REQUESTS_PER_RUN = 6


def model_spec() -> tuple[str, str]:
    """Return (provider, model name) from MODEL in .env."""
    spec = (os.getenv("MODEL") or DEFAULT_MODEL).strip()
    provider, _, name = spec.partition(":")
    provider = provider.lower()
    if provider not in PROVIDER_KEYS or not name:
        raise ValueError(
            f"MODEL={spec!r} is not usable. Expected '<provider>:<model>' where "
            f"provider is one of {', '.join(sorted(PROVIDER_KEYS))}."
        )
    return provider, name


def build_model() -> ConcurrencyLimitedModel:
    """The one model every agent shares.

    The concurrency cap exists for the research pipeline: it fires several agents
    at once, which is exactly how you earn a 429.
    """
    provider, name = model_spec()
    inner: Model
    if provider == "google":
        inner = GoogleModel(
            name,
            provider=GoogleProvider(
                retry_options=HttpRetryOptions(
                    attempts=4,
                    initial_delay=2,
                    max_delay=30,
                    http_status_codes=[429, 500, 502, 503, 504],
                )
            ),
        )
    else:
        inner = OpenRouterModel(name, provider=OpenRouterProvider())
    return ConcurrencyLimitedModel(inner, limiter=2)


_model: ConcurrencyLimitedModel | None = None


def get_model() -> ConcurrencyLimitedModel:
    """Build the shared model on first use, so importing this module needs no key."""
    global _model
    if _model is None:
        _model = build_model()
    return _model


INSTRUCTIONS = """\
You are a concise assistant.
Answer in one or two short sentences.
No preamble, no restating the question, no bullet lists unless asked.
If you don't know, say so in one sentence.\
"""


def get_chat_agent() -> Agent:
    """The short-answer chat agent behind the Chat tab."""
    return Agent(get_model(), instructions=INSTRUCTIONS)


def check_backend() -> str | None:
    """Return an error message if the model or its key is unusable, otherwise None."""
    try:
        provider, _ = model_spec()
    except ValueError as exc:
        return str(exc)
    key = PROVIDER_KEYS[provider]
    if not os.getenv(key):
        return f"{key} is not set. Put it in the .env file and restart the app."
    return None


if __name__ == "__main__":
    # Quick terminal test: python agent.py
    # Model replies are full Unicode; the Windows console is cp1252.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    error = check_backend()
    if error:
        raise SystemExit(error)
    print(f"Using {':'.join(model_spec())}")
    try:
        result = get_chat_agent().run_sync("What is Pydantic AI in one sentence?")
    except Exception as exc:
        raise SystemExit(f"Request failed: {exc}")
    print(result.output)
