from dataclasses import dataclass

from apps.home.ampa.entities import HomeBloodPressureRegistry


@dataclass(frozen=True, slots=True)
class CreateRegistryItem:
    datetime: str
    registry: HomeBloodPressureRegistry


@dataclass(frozen=True, slots=True)
class GetRegistryItem:
    result_id: str


@dataclass(frozen=True, slots=True)
class RegistryItem:
    datetime: str
    result_id: str
    registry: HomeBloodPressureRegistry
