import logging
from typing import Any, Callable
from zoneinfo import ZoneInfo

from pydantic import BaseModel

from .llm_policies import LLMPolicy
from .llm_types import LLMInvoker

logger = logging.getLogger(__name__)


class LLMWithFallback(LLMInvoker):
    QUOTA_KEYWORDS = [
        "quota",
        "rate limit",
        "429",
        "resource exhausted",
    ]

    FAILED_MODELS_KEY = "llm_failed_models"
    FAILED_MODELS_DATE_KEY = "llm_failed_models_date"

    def __init__(
        self, model_factory, models: list[str], api_key: str, policy: LLMPolicy
    ):
        self.model_factory = model_factory
        self.models = models
        self.api_key = api_key
        self.policy = policy
        self.tz = ZoneInfo("US/Pacific")

    def invoke(self, messages, **kwargs) -> Any:
        return self._execute_with_fallback(lambda llm: llm.invoke(messages, **kwargs))

    def invoke_structured(
        self,
        messages,
        schema: BaseModel,
        method: str = "function_calling",
        strict: bool = True,
        **kwargs,
    ) -> Any:
        def execute(llm):
            structured = llm.with_structured_output(
                schema,
                method=method,
                strict=strict,
            )
            return structured.invoke(messages, **kwargs)

        return self._execute_with_fallback(execute)

    def _execute_with_fallback(self, execute: Callable[[Any], Any]) -> Any:
        last_error = None
        models = self.policy.get_available_models(self.models)
        for model in models:
            llm = self.model_factory(model, self.api_key)
            logger.debug(f"Using model: {model}")

            try:
                return execute(llm)

            except Exception as e:
                if self._is_retryable_error(e):
                    logger.info(f"Quota hit on model: {model}")

                    self.policy.mark_failed(model)

                    last_error = e
                    continue

                raise

        raise Exception(f"All models failed. Last error: {last_error}")

    def _is_retryable_error(self, error: Exception) -> bool:
        msg = str(error).lower()
        return any(k in msg for k in self.QUOTA_KEYWORDS)


def get_llm_with_fallback(
    model_factory, models: list[str], api_key: str, policy: LLMPolicy
):
    return LLMWithFallback(model_factory, models, api_key, policy)
