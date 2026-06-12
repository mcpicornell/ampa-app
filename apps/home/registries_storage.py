import uuid
from typing import Protocol

from django.conf import settings
from django.core.cache import cache

from apps.home.ampa.entities import HomeBloodPressureRegistry
from apps.home.registries_storage_types import (
    CreateRegistryItem,
    GetRegistryItem,
    RegistryItem,
)


class RegiestriesStorage(Protocol):
    def get_registry(self, get_registry_item: GetRegistryItem) -> RegistryItem:
        pass

    def save_registry(self, registry_item: CreateRegistryItem) -> RegistryItem:
        pass


class RegistriesCache(RegiestriesStorage):
    PREFIX = "ampa-result-"

    def get_registry(self, get_registry_item: GetRegistryItem) -> RegistryItem | None:
        registry = cache.get(f"{self.PREFIX}{get_registry_item.result_id}")
        if registry is None:
            return None
        return RegistryItem(
            datetime=registry["datetime"],
            result_id=get_registry_item.result_id,
            registry=HomeBloodPressureRegistry(**registry["registry"]),
        )

    def save_registry(self, registry_item: CreateRegistryItem) -> RegistryItem:
        result_id = str(uuid.uuid4())
        cache.set(
            f"{self.PREFIX}{result_id}",
            {
                "datetime": registry_item.datetime,
                "registry": registry_item.registry.model_dump(),
            },
            timeout=settings.CACHE_EXPIRATION,
        )
        return RegistryItem(
            datetime=registry_item.datetime,
            result_id=result_id,
            registry=registry_item.registry,
        )


def get_registries_storage() -> RegiestriesStorage:
    return RegistriesCache()
