from dataclasses import asdict
from functools import lru_cache

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from apps.home.ampa.entities import HomeBloodPressureRegistry
from apps.home.ampa.entities.ampa_result import AmpaResult
from apps.home.ampa.services import (
    AmpaReaderAgent,
    AmpaResultCalculator,
    HomeBloodPressureFilter,
    LocalJsonService,
    get_ampa_reader_agent,
    get_ampa_result_calculator,
    get_home_blood_pressure_filter,
    get_local_json_service,
)
from apps.home.ampa.utils import build_fake_registry


class AmpaFileController:
    def __init__(
        self,
        local_json_service: LocalJsonService,
        filter_service: HomeBloodPressureFilter,
        calculator: AmpaResultCalculator,
        ampa_reader_agent: AmpaReaderAgent,
    ):
        self._local_json_service = local_json_service
        self._filter_service = filter_service
        self._calculator = calculator
        self._ampa_reader_agent = ampa_reader_agent

    def calculate_ampa_result(
        self, registry: HomeBloodPressureRegistry, datetime_str: str
    ) -> AmpaResult:
        registry_filtered = self._filter_service.filter(registry)
        self._local_json_service.write_json(
            f"ampa_registry_filtered_{datetime_str}.json",
            registry_filtered.model_dump(),
        )
        result = self._calculator.calculate(registry_filtered)
        self._local_json_service.write_json(
            f"ampa_result_{datetime_str}.json", asdict(result)
        )
        return result

    def upload_ampa_file(
        self, file: UploadedFile, datetime_str: str
    ) -> HomeBloodPressureRegistry:
        if settings.LLM_RESPONSE_HARDCODED:
            return build_fake_registry()

        registry = self._ampa_reader_agent.read_ampa(file)

        # Save to local JSON for debugging
        self._local_json_service.write_json(
            f"ampa_registry_{datetime_str}.json", registry.model_dump()
        )

        return registry


@lru_cache
def get_ampa_file_controller() -> AmpaFileController:
    return AmpaFileController(
        local_json_service=get_local_json_service(settings.LOCAL_JSON_DIR),
        filter_service=get_home_blood_pressure_filter(),
        calculator=get_ampa_result_calculator(),
        ampa_reader_agent=get_ampa_reader_agent(),
    )
