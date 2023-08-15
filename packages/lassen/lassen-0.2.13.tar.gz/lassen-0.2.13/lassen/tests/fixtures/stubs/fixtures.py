from datetime import datetime
from enum import Enum

from lassen.stubs.base import BaseStub
from lassen.stubs.field import Field
from lassen.stubs.generators import SchemaGenerator, StoreGenerator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import timezone


class SimpleEnum(Enum):
    TEST = "TEST"


class UserStub(BaseStub):
    store_gen = StoreGenerator("stores")
    schema_gen = SchemaGenerator("schemas")
    public_schema_gen = SchemaGenerator("schemas_public")

    first_name: str = Field(description="First name of the user", examples=["John"])
    last_name: str | None = Field(description="Last name of the user", examples=["Smith"])

    password: str = Field(create=True)

    enum_value: SimpleEnum = Field(generators=[store_gen, schema_gen])

    creation_date: datetime = Field(
        generators=[store_gen, schema_gen], default=lambda: datetime.now()
    )

    # A timezone won't technically get cast properly, but we use it as a demonstration
    # of the forward reference capability
    forward_reference_value: 'timezone' = Field(
        generators=[store_gen, schema_gen]
    )
