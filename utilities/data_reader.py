from __future__ import annotations

import json
from dataclasses import fields
from pathlib import Path
from typing import Any, TypeVar

T = TypeVar("T")


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def load_dataclass_records(path: Path, factory: type[T]) -> list[T]:
    records = read_json(path)
    valid_names = {field.name for field in fields(factory)}
    return [factory(**{key: value for key, value in record.items() if key in valid_names}) for record in records]
