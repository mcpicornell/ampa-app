import json
from functools import lru_cache
from pathlib import Path


class LocalJsonService:
    def __init__(self, json_path: str | Path):
        self._json_path = Path(json_path)

    def read_json(self, filename: str) -> dict:
        with open(self._json_path / filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def write_json(self, filename: str, data: dict) -> None:
        with open(self._json_path / filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


@lru_cache
def get_local_json_service(json_path: str | Path) -> LocalJsonService:
    return LocalJsonService(json_path)
