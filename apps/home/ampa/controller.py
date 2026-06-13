import datetime
from dataclasses import asdict, dataclass
from typing import BinaryIO

from .entities import (
    AmpaResult,
    FilteredHomeBloodPressureRegistry,
    HomeBloodPressureRegistry,
)
from .services import (
    AMPAImagesStorage,
    AmpaReaderAgent,
    AmpaResultCalculator,
    HomeBloodPressureFilter,
    LocalJsonService,
)
from .utils import file_binary_to_base64


@dataclass(frozen=True, slots=True)
class AmpaFileControllerDependencies:
    storage_service: AMPAImagesStorage
    local_json_service: LocalJsonService
    filter_service: HomeBloodPressureFilter
    calculator: AmpaResultCalculator
    ampa_reader_agent: AmpaReaderAgent
    json_debug_active: bool = False


class AmpaFileController:
    def __init__(
        self,
        dependencies: AmpaFileControllerDependencies,
    ):
        self._dependencies = dependencies

    def save_ampa_file(self, file: BinaryIO) -> str:
        img_base64 = file_binary_to_base64(file)
        registry_id = self._dependencies.storage_service.save_img(img_base64)
        return registry_id

    def calculate_ampa_result(self, registry_id: str) -> AmpaResult:
        image_base64: str = self._dependencies.storage_service.get_img(registry_id)
        if not image_base64:
            raise ValueError(f"Image for registry '{registry_id}' not found")

        registry: HomeBloodPressureRegistry = self._read_ampa_img_from_agent(
            image_base64
        )
        registry_filtered: FilteredHomeBloodPressureRegistry = self._filter_registry(
            registry
        )
        result: AmpaResult = self._calculate_result(registry_filtered)
        return result

    def _read_ampa_img_from_agent(self, image_base64: str) -> HomeBloodPressureRegistry:
        registry = self._dependencies.ampa_reader_agent.read_ampa(image_base64)
        self._write_json("ampa_registry", registry.model_dump())
        return registry

    def _filter_registry(
        self, registry: HomeBloodPressureRegistry
    ) -> FilteredHomeBloodPressureRegistry:
        registry_filtered = self._dependencies.filter_service.filter(registry)
        self._write_json("ampa_registry_filtered", asdict(registry_filtered))
        return registry_filtered

    def _calculate_result(
        self, registry_filtered: FilteredHomeBloodPressureRegistry
    ) -> AmpaResult:
        result = self._dependencies.calculator.calculate(registry_filtered)
        self._write_json("ampa_result", asdict(result))
        return result

    def _write_json(self, filename: str, data: dict):
        if self._dependencies.json_debug_active:
            datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename_with_datetime = f"{filename}_{datetime_str}.json"
            self._dependencies.local_json_service.write_json(
                filename_with_datetime, data
            )


def get_ampa_file_controller(
    dependencies: AmpaFileControllerDependencies,
) -> AmpaFileController:

    return AmpaFileController(dependencies)
