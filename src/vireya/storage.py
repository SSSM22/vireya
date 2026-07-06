from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class JsonStore:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path or "data/vireya.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def load(self) -> Dict[str, Any]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, data: Dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def append(self, key: str, value: Any) -> None:
        data = self.load()
        bucket = data.setdefault(key, [])
        if not isinstance(bucket, list):
            raise TypeError(f"{key} is not a list")
        bucket.append(value)
        self.save(data)

    def get(self, key: str, default: Any = None) -> Any:
        return self.load().get(key, default)
