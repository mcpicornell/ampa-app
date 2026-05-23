from apps.home.ampa.entities import HomeBloodPressureRegistry
from apps.home.ampa.llm import get_llm
from apps.home.ampa.services.prompts import AMPA_SYSTEM_PROMPT


class AmpaReaderAgent:
    def read_ampa(self, file: str) -> HomeBloodPressureRegistry:
        llm = get_llm()

        llm_structured = llm.with_structured_output(
            HomeBloodPressureRegistry, method="json_schema", strict=True
        )

        return llm_structured.invoke(
            [
                {"role": "system", "content": AMPA_SYSTEM_PROMPT},
                {"role": "user", "content": f"Extract AMPA data from file: {file}"},
            ]
        )
