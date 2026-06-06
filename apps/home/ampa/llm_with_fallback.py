import datetime
import logging

from django.core.cache import cache
from pydantic import BaseModel

logger = logging.getLogger(__name__)

MODELS = (
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
)

FAILED_MODELS_KEY = "llm_failed_models"
FAILED_MODELS_DATE_KEY = "llm_failed_models_date"


class LLMWithFallback:
    QUOTA_KEYWORDS = [
        "quota",
        "rate limit",
        "429",
        "resource exhausted",
    ]

    def __init__(self, model_factory):
        self.model_factory = model_factory

    def invoke_with_structured_output(
        self,
        messages,
        pydantic_model: BaseModel,
        method: str = "function_calling",
        strict: bool = True,
    ):
        last_error = None
        failed_models = self._get_failed_models()

        for model in MODELS:
            if model in failed_models:
                logger.debug(f"Skipping failed model: {model}")
                continue

            llm = self.model_factory(model)
            logger.debug(f"Using model: {model}")

            try:
                if model == "gemini-2.0-flash-lite":
                    raise Exception("quota")
                structured = llm.with_structured_output(
                    pydantic_model,
                    method=method,
                    strict=strict,
                )

                return structured.invoke(messages)

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

    def _get_failed_models(self):
        today = str(datetime.date.today())

        cached_date = cache.get(FAILED_MODELS_DATE_KEY)

        if cached_date != today:
            cache.set(FAILED_MODELS_DATE_KEY, today, timeout=None)
            cache.set(FAILED_MODELS_KEY, [], timeout=None)
            return set()

        return set(cache.get(FAILED_MODELS_KEY, []) or [])

    def _add_failed_model(self, model: str):
        failed = list(self._get_failed_models())

        if model not in failed:
            failed.append(model)
        logger.info(f"Adding failed model to cache: {model}")
        cache.set(FAILED_MODELS_KEY, failed, timeout=None)


def get_llm_with_fallback(model_factory):
    return LLMWithFallback(model_factory)
