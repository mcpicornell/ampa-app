from django.core.files.uploadedfile import UploadedFile
from langchain_core.messages import HumanMessage, SystemMessage

from ...entities import HomeBloodPressureRegistry
from ..llms import LLMWithFallback, get_llm_with_fallback
from ..llms import get_google_llm as llm_factory
from ..utils import encode_image
from .prompts import READ_AMPA_SYSTEM_PROMPT


class AmpaReaderAgent:
    def __init__(self, llm: LLMWithFallback):
        self._llm = llm

    def read_ampa(self, file: UploadedFile) -> HomeBloodPressureRegistry:
        try:
            file.seek(0)
            image_base64 = encode_image(file)
            messages = self._build_messages(READ_AMPA_SYSTEM_PROMPT, image_base64)
            result = self._llm.invoke_with_structured_output(
                messages, HomeBloodPressureRegistry, "function_calling", True
            )
            return result
        except Exception as e:
            raise Exception(f"Error reading AMPA file from Agent: {e}") from e

    def _build_messages(self, system_prompt: str, image_base64: str) -> list:
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


def get_ampa_reader_agent(models: list[str]) -> AmpaReaderAgent:
    llm = get_llm_with_fallback(llm_factory, models)
    return AmpaReaderAgent(llm)
