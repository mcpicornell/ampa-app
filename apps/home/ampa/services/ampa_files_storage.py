import uuid
from functools import lru_cache
from typing import BinaryIO, Protocol

from django.conf import settings
from django.core.cache import cache


class AMPAImagesStorage(Protocol):
    def save_img(self, file: BinaryIO) -> str:
        pass

    def get_img(self, registry_id: str) -> str | None:
        pass


class AMPAImagesCache(AMPAImagesStorage):
    PREFIX = "ampa-registry-"

    def save_img(self, img_base64: str) -> str:
        registry_id = str(uuid.uuid4())
        cache.set(
            f"{self.PREFIX}{registry_id}",
            img_base64,
            timeout=settings.CACHE_EXPIRATION,
        )
        return registry_id

    def get_img(self, registry_id: str) -> str | None:
        return cache.get(f"{self.PREFIX}{registry_id}")


@lru_cache
def get_ampa_images_storage() -> AMPAImagesStorage:
    return AMPAImagesCache()
