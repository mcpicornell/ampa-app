import threading
import uuid
from functools import lru_cache
from typing import BinaryIO, Protocol

from cachetools import TTLCache


class AMPAImagesStorage(Protocol):
    def save_img(self, file: BinaryIO) -> str:
        pass

    def get_img(self, registry_id: str) -> str | None:
        pass


class AMPAImagesCache(AMPAImagesStorage):
    PREFIX = "ampa-registry-"

    def __init__(self, max_size: int, ttl_seconds: int):
        self._internal_memory_cache = TTLCache(maxsize=max_size, ttl=ttl_seconds)
        self._cache_lock = threading.Lock()

    def save_img(self, img_base64: str) -> str:
        registry_id = str(uuid.uuid4())
        key = f"{self.PREFIX}{registry_id}"
        with self._cache_lock:
            self._internal_memory_cache[key] = img_base64
        return registry_id

    def get_img(self, registry_id: str) -> str | None:
        key = f"{self.PREFIX}{registry_id}"
        with self._cache_lock:
            return self._internal_memory_cache.get(key)


@lru_cache
def get_ampa_images_storage(
    max_size: int = 100, ttl_seconds: int = 1800
) -> AMPAImagesStorage:
    return AMPAImagesCache(
        max_size=max_size,
        ttl_seconds=ttl_seconds,
    )
