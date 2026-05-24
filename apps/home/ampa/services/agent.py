from functools import lru_cache

from langchain_core.messages import HumanMessage, SystemMessage

from apps.home.ampa.entities import HomeBloodPressureRegistry
from apps.home.ampa.llm import get_google_llm as get_llm
from apps.home.ampa.services.prompts import AMPA_SYSTEM_PROMPT
from apps.home.ampa.services.utils import encode_image


class AmpaReaderAgent:
    def read_ampa(self, file) -> HomeBloodPressureRegistry:
        try:
            llm = get_llm()

            llm_structured = llm.with_structured_output(
                HomeBloodPressureRegistry, method="json_schema", strict=True
            )
            file.seek(0)
            image_base64 = encode_image(file)
            return llm_structured.invoke(
                [
                    SystemMessage(content=AMPA_SYSTEM_PROMPT),
                    HumanMessage(
                        content=[
                            {
                                "type": "text",
                                "text": "Extract AMPA data from this image.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                },
                            },
                        ]
                    ),
                ]
            )
        except Exception as e:
            raise Exception("Error reading AMPA file from Agent") from e


@lru_cache
def get_ampa_reader_agent() -> AmpaReaderAgent:
    return AmpaReaderAgent()
