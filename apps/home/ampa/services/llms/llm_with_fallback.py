import datetime
import logging
from typing import Any, Callable
from zoneinfo import ZoneInfo

from cachetools import TTLCache
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class LLMWithFallback:
    QUOTA_KEYWORDS = [
        "quota",
        "rate limit",
        "429",
        "resource exhausted",
    ]
    _cache = TTLCache(maxsize=100, ttl=86400)
    FAILED_MODELS_KEY = "llm_failed_models"
    FAILED_MODELS_DATE_KEY = "llm_failed_models_date"

    def __init__(self, model_factory, models: list[str], api_key: str):
        self.model_factory = model_factory
        self.models = models
        self.api_key = api_key
        self.tz = ZoneInfo("US/Pacific")  # US/Pacific time is when Gemini reset quotas

    def invoke(self, messages, **kwargs) -> Any:
        def execute(llm):
            return llm.invoke(messages, **kwargs)

        return self._execute_with_fallback(execute)

    def invoke_with_structured_output(
        self,
        messages,
        pydantic_model: BaseModel,
        method: str = "function_calling",
        strict: bool = True,
        **kwargs,
    ) -> Any:
        def execute(llm):
            structured = llm.with_structured_output(
                pydantic_model,
                method=method,
                strict=strict,
            )
            return structured.invoke(messages, **kwargs)

        return self._execute_with_fallback(execute)

    def _execute_with_fallback(self, execute: Callable[[Any], Any]) -> Any:
        last_error = None
        failed_models = self._get_failed_models()

        for model in self.models:
            if model in failed_models:
                logger.debug(f"Skipping failed model: {model}")
                continue

            llm = self.model_factory(model, self.api_key)
            logger.debug(f"Using model: {model}")

            try:
                return execute(llm)

            except Exception as e:
                if self._is_retryable_error(e):
                    self._add_failed_model(model)
                    last_error = e
                    continue
                raise

        raise Exception(f"All models failed. Last error: {last_error}")

    def _is_retryable_error(self, error: Exception) -> bool:
        msg = str(error).lower()
        return any(k in msg for k in self.QUOTA_KEYWORDS)

    def _add_failed_model(self, model: str) -> None:
        failed = list(self._get_failed_models())

        if model not in failed:
            failed.append(model)
        logger.info(f"Adding failed model to cache: {model}")
        self._cache[self.FAILED_MODELS_KEY] = failed

    def _get_failed_models(self) -> set[str]:
        today: str = self._get_today(self.tz)
        cached_date = self._cache.get(self.FAILED_MODELS_DATE_KEY)
        if cached_date != today:
            self._cache[self.FAILED_MODELS_DATE_KEY] = today
            self._cache[self.FAILED_MODELS_KEY] = []
            return set()

        return set(self._cache.get(self.FAILED_MODELS_KEY, []) or [])

    def _get_today(self, tz: ZoneInfo = ZoneInfo("US/Pacific")) -> str:
        return str(datetime.datetime.now(tz).date())


def get_llm_with_fallback(model_factory, models: list[str], api_key: str):
    return LLMWithFallback(model_factory, models, api_key)
