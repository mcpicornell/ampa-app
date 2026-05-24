from functools import lru_cache

from apps.home.ampa.entities import HomeBloodPressureRegistry
from apps.home.ampa.entities.ampa_result import AmpaResult
from apps.home.ampa.services import (
    get_ampa_reader_agent,
    get_ampa_result_calculator,
    get_home_blood_pressure_filter,
)
from django.conf import settings
from apps.home.ampa.utils import build_fake_registry


class AmpaFileController:
    def calculate_ampa_result(self, data: dict[str, any]) -> AmpaResult:
        registry = HomeBloodPressureRegistry(**data)
        filter_service = get_home_blood_pressure_filter()
        registry_filtered = filter_service.filter(registry)

        calculator = get_ampa_result_calculator()
        return calculator.calculate(registry_filtered)

    def upload_ampa_file(self, file) -> HomeBloodPressureRegistry:

        if settings.LLM_RESPONSE_HARDCODED:
            return build_fake_registry()

        
        agent = get_ampa_reader_agent()
        return agent.read_ampa(file)


@lru_cache
def get_ampa_file_controller() -> AmpaFileController:
    return AmpaFileController()
