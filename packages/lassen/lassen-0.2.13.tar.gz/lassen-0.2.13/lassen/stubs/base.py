from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Type

from pydantic import BaseModel

if TYPE_CHECKING:
    from lassen.stubs.generators.common import ExtractedStubImports


@dataclass
class RenderedFile:
    content: str
    created_classes: list[str]


class BaseDefinition(ABC, BaseModel):
    """
    A Definition can provide additional metadata to generators so they can implement
    their own parsing logic.
    """


class BaseStub(ABC):
    """
    A Stub is the core definition class that users leverage to define their data schema.
    It serves as the ground truth for the model that is used in the database and within
    most CRUD API endpoints that are fronting the database.
    """


class BaseGenerator(ABC):
    """
    A Generator takes input Stub definition and translates it to code definition files
    that will actually be used by the client application. They allow one stub file to
    be repurposed for Pydantic, SQLAlchemy, etc.
    """

    output_directory: str

    def __init__(self, output_directory: str):
        self.output_directory = output_directory

    @abstractmethod
    def __call__(
        self, model: Type[BaseStub], import_hints: "ExtractedStubImports"
    ) -> RenderedFile:
        pass
