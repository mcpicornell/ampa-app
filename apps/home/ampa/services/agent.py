from django.core.files.uploadedfile import UploadedFile
from langchain_core.messages import HumanMessage, SystemMessage

from apps.home.ampa.entities import HomeBloodPressureRegistry
from apps.home.ampa.services.prompts import AMPA_SYSTEM_PROMPT
from apps.home.ampa.services.utils import encode_image


class AmpaReaderAgent:
    def __init__(self, llm):
        self._llm = llm

    def read_ampa(self, file: UploadedFile) -> HomeBloodPressureRegistry:
        try:
            file.seek(0)
            image_base64 = encode_image(file)
            llm_structured = self._llm.with_structured_output(
                HomeBloodPressureRegistry, method="function_calling", strict=True
            )
            image_url = f"data:image/jpeg;base64,{image_base64}"
            result = llm_structured.invoke(
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
                                "image_url": {"url": image_url},
                            },
                        ]
                    ),
                ]
            )
            print("A6 - after invoke")
            return result
        except Exception as e:
            raise Exception(f"Error reading AMPA file from Agent: {e}") from e


def get_ampa_reader_agent(llm) -> AmpaReaderAgent:
    return AmpaReaderAgent(llm)
