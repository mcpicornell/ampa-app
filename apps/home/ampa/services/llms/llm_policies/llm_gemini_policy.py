import time
from datetime import datetime, timedelta
from functools import lru_cache
from zoneinfo import ZoneInfo

from .llm_policy_types import LLMPolicy


class GeminiPolicy(LLMPolicy):
    def __init__(self, models: list[str]):
        self._models = models
        self._blocked_until: dict[str, float] = {}

    def is_blocked(self, model: str) -> bool:
        until = self._blocked_until.get(model)
        return until is not None and time.time() < until

    def mark_failed(self, model: str):
        self._blocked_until[model] = self._next_reset_timestamp()

    def available_models(self, models: list[str]) -> list[str]:
        return [m for m in models if not self.is_blocked(m)]

    def _next_reset_timestamp(self) -> float:
        tz = ZoneInfo("America/Los_Angeles")
        now = datetime.now(tz)

        reset = now.replace(hour=9, minute=0, second=0, microsecond=0)

        if now >= reset:
            reset += timedelta(days=1)

        return reset.timestamp()


@lru_cache
def get_gemini_policy(models: list[str]) -> GeminiPolicy:
    return GeminiPolicy(models)
