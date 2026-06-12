from functools import lru_cache

from .llm_policies import LLMPolicy
from .llm_router import Router, get_llm_router


class LLMLiteService:
    def __init__(
        self, router: Router, policy: LLMPolicy, models: tuple[str, ...], api_key: str
    ):
        self._router = router
        self._policy = policy
        self._models = models
        self._api_key = api_key

    def invoke(self, messages, **kwargs):
        model = self._get_model()

        try:
            return self._router.completion(
                model=model, messages=messages, api_key=self._api_key, **kwargs
            )

        except Exception as e:
            if "429" in str(e).lower():
                self._policy.block_until_reset(model)

                fallback = self._next_model(model)

                return self._router.completion(
                    model=fallback, messages=messages, api_key=self._api_key, **kwargs
                )

            raise

    def invoke_structured(self, messages, schema, **kwargs):
        model = self._get_model()

        try:
            return self._router.completion(
                model=model,
                messages=messages,
                response_format=schema,
                api_key=self._api_key,
                **kwargs,
            )

        except Exception as e:
            if "429" in str(e).lower():
                self._policy.block_until_reset(model)

                fallback = self._next_model(model)

                return self._router.completion(
                    model=fallback,
                    messages=messages,
                    response_format=schema,
                    api_key=self._api_key,
                    **kwargs,
                )

            raise

    def _get_model(self):
        for m in self._models:
            if not self._policy.is_blocked(m):
                return m
        raise Exception("No available AI models, all models are blocked")

    def _next_model(self, current):
        idx = self._models.index(current)
        return self._models[min(idx + 1, len(self._models) - 1)]


@lru_cache
def get_llm_lite_service(
    policy: LLMPolicy, models: tuple[str, ...], api_key: str, router: Router
):
    return LLMLiteService(
        router=router,
        policy=policy,
        models=models,
        api_key=api_key,
    )
