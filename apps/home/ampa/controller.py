from dataclasses import asdict
from functools import lru_cache

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from .constants import GEMINI_MODELS
from .entities import AmpaResult, HomeBloodPressureRegistry
from .services import (
    AmpaReaderAgent,
    AmpaResultCalculator,
    HomeBloodPressureFilter,
    LocalJsonService,
    get_ampa_reader_agent,
    get_ampa_result_calculator,
    get_home_blood_pressure_filter,
    get_local_json_service,
)
from .utils import build_fake_registry


class AmpaFileController:
    def __init__(
        self,
        local_json_service: LocalJsonService,
        filter_service: HomeBloodPressureFilter,
        calculator: AmpaResultCalculator,
        ampa_reader_agent: AmpaReaderAgent,
        json_debug_active: bool = False,
    ):
        self._local_json_service = local_json_service
        self._filter_service = filter_service
        self._calculator = calculator
        self._ampa_reader_agent = ampa_reader_agent
        self._json_debug_active = json_debug_active

    def calculate_ampa_result(
        self, registry: HomeBloodPressureRegistry, datetime_str: str
    ) -> AmpaResult:
        registry_filtered = self._filter_service.filter(registry)
        self._write_json(
            f"ampa_registry_filtered_{datetime_str}.json",
            registry_filtered.model_dump(),
        )
        result = self._calculator.calculate(registry_filtered)
        self._write_json(f"ampa_result_{datetime_str}.json", asdict(result))
        return result

    def upload_ampa_file(
        self, file: UploadedFile, datetime_str: str
    ) -> HomeBloodPressureRegistry:
        if settings.LLM_RESPONSE_HARDCODED:
            return build_fake_registry()

        registry = self._ampa_reader_agent.read_ampa(file)

        self._write_json(f"ampa_registry_{datetime_str}.json", registry.model_dump())

        return registry

    def _write_json(self, filename: str, data: dict):
        if self._json_debug_active:
            self._local_json_service.write_json(filename, data)


@lru_cache
def get_ampa_file_controller(json_debug_active: bool = False) -> AmpaFileController:
    return AmpaFileController(
        local_json_service=get_local_json_service(settings.LOCAL_JSON_DIR),
        filter_service=get_home_blood_pressure_filter(),
        calculator=get_ampa_result_calculator(),
        ampa_reader_agent=get_ampa_reader_agent(GEMINI_MODELS),
        json_debug_active=json_debug_active,
    )
