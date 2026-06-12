from typing import BinaryIO

from langchain_core.messages import HumanMessage, SystemMessage

from apps.home.ampa.services.llms.llm_lite_service import LLMLiteService

from ...entities import HomeBloodPressureRegistry
from ..llms import (
    LLMInvoker,
    LLMPolicy,
    LLMWithFallback,
    get_llm_lite_service,
    get_llm_with_fallback,
)
from ..llms import get_google_llm as llm_factory
from ..llms.llm_router import Router
from ..utils import encode_image
from .prompts import READ_AMPA_SYSTEM_PROMPT


class AmpaReaderAgent:
    def __init__(self, llm: LLMInvoker):
        self._llm = llm

    def read_ampa(self, file: BinaryIO) -> HomeBloodPressureRegistry:
        try:
            file.seek(0)
            image_base64 = encode_image(file)
            messages = self._build_messages(READ_AMPA_SYSTEM_PROMPT, image_base64)
            result = self._llm.invoke_structured(
                messages,
                HomeBloodPressureRegistry,
            )
            return result
        except Exception as e:
            raise Exception(f"Error reading AMPA file from Agent: {e}") from e

    def _build_messages(self, system_prompt: str, image_base64: str) -> list:
        if isinstance(self._llm, LLMWithFallback):
            return self._build_langchain_messages(system_prompt, image_base64)
        elif isinstance(self._llm, LLMLiteService):
            return self.build_messages_litellm(system_prompt, image_base64)
        raise ValueError(f"Unsupported LLM type: {type(self._llm)}")

    def _build_langchain_messages(self, system_prompt: str, image_base64: str) -> list:
        image_url = f"data:image/jpeg;base64,{image_base64}"
        return [
            SystemMessage(content=system_prompt),
            HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": "Extract AMPA data from this image.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ]
            ),
        ]

    def build_messages_litellm(
        self, system_prompt: str, image_base64: str
    ) -> list[dict]:
        image_url = f"data:image/jpeg;base64,{image_base64}"
        return [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract AMPA data from this image.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ],
            },
        ]


def get_ampa_reader_agent(models: list[str], api_key: str, **kwargs) -> AmpaReaderAgent:
    llm = get_llm_with_fallback(llm_factory, models, api_key)
    return AmpaReaderAgent(llm)


def get_ampa_reader_agent_litellm(
    models: tuple[str, ...], api_key: str, policy: LLMPolicy, router: Router
) -> AmpaReaderAgent:
    llm = get_llm_lite_service(policy, models, api_key, router)
    return AmpaReaderAgent(llm)
