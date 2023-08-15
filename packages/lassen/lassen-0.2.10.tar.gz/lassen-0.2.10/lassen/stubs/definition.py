from typing import Any

from lassen.stubs.base import BaseDefinition


class UniqueDefinition(BaseDefinition):
    name: str
    fields: list[Any]
