from typing import Protocol

from pydantic import BaseModel


class LLMInvoker(Protocol):
    def invoke_structured(
        self, messages: list, schema: BaseModel, **kwargs
    ) -> object: ...
    def invoke(self, messages: list, **kwargs) -> str: ...
