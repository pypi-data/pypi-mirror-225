from typing import Type, Union

from sqlalchemy.orm import aliased
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column

from lassen.db.base_class import Base


def get_class_by_classname(base, classname: str):
    """
    Return class reference mapped to the table.

    Allows clients to resolve relationship definitions, like:
    parent = relationship("Parent")

    """
    for mapper in base.registry.mappers:
        cls = mapper.class_
        if not classname.startswith("_"):
            if cls.__name__ == classname:
                return cls
    raise ValueError(f"Class not found: {classname}")


class chain_select:
    """
    To access data across multiple tables ideally you'd be able to do
    something like this:

        Child.parent.parent.identifier

    This isn't valid syntax, since `parent` is an InstrumentedAttribute of
    the class it doesn't allow this kind of chaining. Users can only use this
    syntax once they actually have an instance of the ORM model, which doesn't
    help during selection.

    This class provides some syntactic sugar to allow this kind of chaining during
    selection. It's used like this:

        chain_select(Child.parent)(Parent.parent)(Parent.identifier)

    """

    def __init__(self, relationship_attr: InstrumentedAttribute):
        self.query_elements: list[InstrumentedAttribute | Column] = []
        self.joins: list[
            tuple[
                Type[Union[InstrumentedAttribute, Column]],
                Type[Union[InstrumentedAttribute, Column]],
            ]
        ] = []

        self._current_model = relationship_attr.parent.class_

        # Now process the passed relationship
        self(relationship_attr)

    def __call__(
        self, *relationship_or_column: InstrumentedAttribute | Column
    ) -> "chain_select":
        if len(relationship_or_column) == 0:
            raise ValueError("Must provide at least one relationship or column")

        first_column = relationship_or_column[0]
        is_relationship = isinstance(
            first_column, InstrumentedAttribute
        ) and isinstance(first_column.property, RelationshipProperty)
        if is_relationship and len(relationship_or_column) > 1:
            raise ValueError(
                "Cannot provide multiple relationships\n"
                "If you need to make multiple queries at different levels of "
                "the chain, you can create multiple chains."
            )

        if is_relationship:
            # Create alias and set join condition
            rel_property = first_column.property
            alias = aliased(get_class_by_classname(Base, rel_property.argument))
            join_condition = list(rel_property.local_columns)[0] == alias.id
            self.joins.append((alias, join_condition))

            # Set the current model to the related model for the next chain
            self.query_elements += [
                getattr(self._current_model, list(rel_property.local_columns)[0].name),
                alias.id,
            ]
            self._current_model = alias

            return self
        else:
            # It's a standard column that is requesting data
            # We want to get all of the columns from the alias, since we've
            # already represented the current state of the chain by the alias
            self.query_elements += [
                getattr(self._current_model, x.name) for x in relationship_or_column
            ]

            # self.query_elements += relationship_or_column
            return self
