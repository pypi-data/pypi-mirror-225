from typing import Any, Callable

from pydantic import BaseModel

from lassen.enums import FilterTypeEnum
from lassen.stubs.base import BaseGenerator


class UNSET_VALUE:
    pass


class FieldDefinition(BaseModel):
    generators: list[BaseGenerator] | None
    description: str | None
    examples: list[Any]
    create: bool
    update: bool
    read: bool
    filter: bool
    filter_extensions: list[FilterTypeEnum] | UNSET_VALUE
    index: bool
    is_relationship: bool
    association_proxy: tuple[str, str] | UNSET_VALUE
    primary_key: bool | UNSET_VALUE
    foreign_key: Any | UNSET_VALUE
    backref: str | UNSET_VALUE
    default: Any | UNSET_VALUE

    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"


def Field(
    generators: list[BaseGenerator] | None = None,
    description: str | None = None,
    examples: list[Any] | None = None,
    create: bool = False,
    update: bool = False,
    read: bool = True,
    filter: bool = False,
    filter_extensions: list[FilterTypeEnum] | UNSET_VALUE = UNSET_VALUE(),
    index: bool = False,
    is_relationship: bool = False,
    association_proxy: tuple[str, str] | UNSET_VALUE = UNSET_VALUE(),
    primary_key: bool | UNSET_VALUE = UNSET_VALUE(),
    foreign_key: Any = UNSET_VALUE(),
    backref: str | UNSET_VALUE = UNSET_VALUE(),
    default: Any | Callable | UNSET_VALUE = UNSET_VALUE(),
) -> Any:
    """
    :param generators: By default, all class-associated generators are used
    :param default: If you want to set a more complex expression as your default
        you can use a lambda x: {my value} expression. This delays execution of
        the actual logic and we'll instead use the lambda values.
    :param If set to True, enables regular equality expressions for this field.
        For additional options, see the filter_extensions parameter.
    :param filter_extensions: List of additional filter extensions
        to enable for this field.

    """
    return FieldDefinition(
        generators=generators,
        description=description,
        examples=examples or [],
        create=create,
        update=update,
        read=read,
        filter=filter,
        filter_extensions=filter_extensions,
        index=index,
        is_relationship=is_relationship,
        association_proxy=association_proxy,
        primary_key=primary_key,
        foreign_key=foreign_key,
        backref=backref,
        default=default,
    )
