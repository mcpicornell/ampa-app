import time
from datetime import datetime, timedelta
from functools import lru_cache
from zoneinfo import ZoneInfo

from .llm_policy_types import LLMPolicy


class GeminiPolicy(LLMPolicy):
    def __init__(self, timezone: ZoneInfo):
        self.timezone = timezone
        self._blocked_until: dict[str, float] = {}
        self._today = datetime.now(timezone).date()

    def is_blocked(self, model: str) -> bool:
        until = self._blocked_until.get(model)
        return until is not None and time.time() < until

    def mark_failed(self, model: str):
        self._blocked_until[model] = self._next_reset_timestamp()

    def get_available_models(self, models: list[str]) -> list[str]:
        self._cleanup_if_new_day()
        return [m for m in models if not self.is_blocked(m)]

    def _next_reset_timestamp(self) -> float:
        now = datetime.now(self.timezone)

        reset = now.replace(hour=9, minute=0, second=0, microsecond=0)

        if now >= reset:
            reset += timedelta(days=1)

        return reset.timestamp()

    def _cleanup_if_new_day(self):
        today = self._current_day()

        if today != self._today:
            self._blocked_until.clear()
            self._today = today

    def _current_day(self) -> str:
        return str(datetime.now(ZoneInfo("America/Los_Angeles")).date())


@lru_cache
def get_gemini_policy(timezone: ZoneInfo) -> GeminiPolicy:
    return GeminiPolicy(timezone)
