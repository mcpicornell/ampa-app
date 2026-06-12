from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..llms import LLMLiteService, LLMWithFallback

if TYPE_CHECKING:
    type LLMInvoker = LLMWithFallback | LLMLiteService
else:
    type LLMInvoker = object
