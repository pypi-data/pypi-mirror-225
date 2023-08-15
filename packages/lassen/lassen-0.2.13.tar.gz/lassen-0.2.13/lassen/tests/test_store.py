from time import time
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Query, Session

from lassen.enums import FilterTypeEnum
from lassen.queries import chain_select
from lassen.store import StoreBase, StoreFilterMixin
from lassen.tests.model_fixtures import (
    SampleChainedChild,
    SampleChainedChildCreate,
    SampleChainedChildFilter,
    SampleChainedChildUpdate,
    SampleChainedParent,
    SampleChainedParentCreate,
    SampleChainedParentUpdate,
    SampleModel,
    SampleSchemaCreate,
    SampleSchemaFilter,
    SampleSchemaUpdate,
)


@pytest.fixture
def use_fixture_models(db_session: Session):
    if not db_session.bind:
        raise ValueError("No database connection")

    from lassen.db.base_class import Base

    Base.metadata.create_all(bind=db_session.bind)


def create_batch(db_session: Session, quantity: int = 1):
    create_identifiers = []
    for i in range(quantity):
        test_model = SampleModel(name=f"Test Model {i}")
        db_session.add(test_model)
        db_session.flush()
        db_session.refresh(test_model)
        create_identifiers.append(test_model.id)
    return create_identifiers


def test_store_base_get(db_session: Session, use_fixture_models):
    test_model_id = create_batch(db_session, quantity=1)[0]

    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)
    # Test with a valid ID
    retrieved = store.get(db_session, id=test_model_id)
    assert retrieved is not None
    assert retrieved.id == test_model_id
    assert retrieved.name == "Test Model 0"

    # Test with an invalid ID
    assert store.get(db_session, id=9999) is None


def test_store_base_get_multi(db_session: Session, use_fixture_models):
    create_batch(db_session, quantity=5)

    store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
    # Test without skip and limit
    retrieved = store.get_multi(db_session, filter=SampleSchemaFilter())
    assert len(retrieved) == 5

    # Test with skip
    retrieved = store.get_multi(db_session, skip=2, filter=SampleSchemaFilter())
    assert len(retrieved) == 3

    # Test with limit
    retrieved = store.get_multi(db_session, limit=2, filter=SampleSchemaFilter())
    assert len(retrieved) == 2

    # Test with skip and limit
    retrieved = store.get_multi(
        db_session, skip=1, limit=2, filter=SampleSchemaFilter()
    )
    assert len(retrieved) == 2


def test_store_base_create(db_session: Session, use_fixture_models):
    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)
    create_schema = SampleSchemaCreate(name="Test Name")
    created = store.create(db_session, obj_in=create_schema)
    db_session.commit()
    assert created.id is not None
    assert created.name == "Test Name"


@pytest.mark.parametrize(
    "return_primaries,quantity,expected_max_time,batch_size",
    [
        (True, 50, 0.1, 100),
        (False, 50, 0.1, 100),
        (True, 5000, 1.0, 100),
        (False, 50000, 4.0, 100),
        (True, 50000, 5.0, 100),
        (False, 50000, 5.0, 1000),
        (True, 50000, 5.0, 1000),
    ],
)
def test_store_bulk_create(
    return_primaries: bool,
    quantity: int,
    expected_max_time: float,
    batch_size: int,
    db_session: Session,
    use_fixture_models,
):
    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)

    start = time()
    element_ids = store.bulk_create(
        db_session,
        [SampleSchemaCreate(name=f"Inserted Name {i}") for i in range(quantity)],
        return_primaries=return_primaries,
        batch_size=batch_size,
    )
    end = time()

    assert end - start < expected_max_time

    if return_primaries:
        assert element_ids
        assert len(element_ids) == quantity

    filter_store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
    all_schemas = filter_store.get_multi(db_session, filter=SampleSchemaFilter())
    assert len(all_schemas) == quantity

    schema_names = {schema.name for schema in all_schemas}
    assert {f"Inserted Name {i}" for i in range(quantity)} == schema_names


def test_store_base_update(db_session: Session, use_fixture_models):
    test_model_id = create_batch(db_session, quantity=1)[0]

    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)
    update_schema = SampleSchemaUpdate(name="Updated Name")
    db_obj = store.get(db_session, id=test_model_id)
    assert db_obj is not None

    updated = store.update(db_session, db_obj=db_obj, obj_in=update_schema)
    db_session.commit()
    assert updated.id == test_model_id
    assert updated.name == "Updated Name"


@pytest.mark.parametrize(
    "quantity,expected_max_time,batch_size",
    [
        (50, 0.1, 100),
        (5000, 2.0, 100),
        (50000, 20.0, 100),
        (50000, 20.0, 1000),
    ],
)
def test_store_bulk_update(
    quantity: int,
    expected_max_time: float,
    batch_size: int,
    db_session: Session,
    use_fixture_models,
):
    test_model_ids = create_batch(db_session, quantity=quantity)
    assert len(test_model_ids) == quantity

    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)

    start = time()
    store.bulk_update(
        db_session,
        [
            (model_id, SampleSchemaUpdate(name=f"Updated Name {i}"))
            for i, model_id in enumerate(test_model_ids)
        ],
        batch_size=batch_size,
    )
    end = time()
    assert end - start < expected_max_time

    db_session.flush()

    filter_store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
    all_models = {
        model.id: model
        for model in filter_store.get_multi(db_session, filter=SampleSchemaFilter())
    }

    for i, model_id in enumerate(test_model_ids):
        updated = all_models[model_id]
        assert updated
        assert updated.id == model_id
        assert updated.name == f"Updated Name {i}"


def test_store_base_remove(db_session: Session, use_fixture_models):
    test_model_id = create_batch(db_session, quantity=1)[0]

    store = StoreBase[SampleModel, SampleSchemaCreate, SampleSchemaUpdate](SampleModel)
    store.remove(db_session, id=test_model_id)
    db_session.commit()

    # Test that the model instance has been removed
    assert store.get(db_session, id=test_model_id) is None


@pytest.mark.parametrize(
    "filter_type,expected_expression",
    [
        (FilterTypeEnum.EQUAL, lambda x, y: x == y),
        (FilterTypeEnum.NOT, lambda x, y: x != y),
        (FilterTypeEnum.IN, lambda x, y: x.in_(y)),
        (FilterTypeEnum.NOT_IN, lambda x, y: ~x.in_(y)),
        (FilterTypeEnum.LESS_THAN, lambda x, y: x < y),
        (FilterTypeEnum.LESS_THAN_OR_EQUAL, lambda x, y: x <= y),
        (FilterTypeEnum.GREATER_THAN, lambda x, y: x > y),
        (FilterTypeEnum.GREATER_THAN_OR_EQUAL, lambda x, y: x >= y),
    ],
)
def test_build_filter(filter_type, expected_expression, use_fixture_models):
    # Mock FilterSchemaType
    mock_filter = MagicMock()
    value = (
        ["mock_name"]
        if filter_type in {FilterTypeEnum.IN, FilterTypeEnum.NOT_IN}
        else "mock_name"
    )
    mock_filter.dict.return_value = {f"name__{filter_type.value}": value}

    # Mock Query
    mock_query = MagicMock(spec=Query)
    mock_query.filter.return_value = MagicMock(
        spec=Query
    )  # Return a new mock query for each filter() call

    store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
    store.build_filter(mock_query, mock_filter, include_archived=True)

    # Check the correct function was called with the right arguments
    # Each accessor to
    expected = expected_expression(SampleModel.name, value)
    call_strings = [str(call[0][0]) for call in mock_query.filter.call_args_list]
    assert str(expected) in call_strings


def test_build_filter_chain(db_session: Session, use_fixture_models):
    parent_store = StoreBase[
        SampleChainedParent, SampleChainedParentCreate, SampleChainedParentUpdate
    ](SampleChainedParent)
    child_store = StoreBase[
        SampleChainedChild, SampleChainedChildCreate, SampleChainedChildUpdate
    ](SampleChainedChild)
    child_filter_store = StoreFilterMixin[SampleChainedChild, SampleChainedChildFilter](
        SampleChainedChild
    )

    parent1 = parent_store.create(
        db_session, obj_in=SampleChainedParentCreate(identifier="parent1")
    )
    parent2 = parent_store.create(
        db_session, obj_in=SampleChainedParentCreate(identifier="parent2")
    )

    child1 = child_store.create(
        db_session,
        obj_in=SampleChainedChildCreate(parent_id=parent1.id),  # type: ignore
    )
    child2 = child_store.create(
        db_session,
        obj_in=SampleChainedChildCreate(parent_id=parent2.id),  # type: ignore
    )

    assert child1.parent_id == parent1.id
    assert child2.parent_id == parent2.id

    parent_identifiers = child_filter_store.get_multi(
        db=db_session,
        filter=SampleChainedChildFilter(),
        only_fetch_columns=[
            chain_select(SampleChainedChild.parent)(SampleChainedParent.identifier)
        ],
    )
    parent_identifiers
    assert len(parent_identifiers) == 2
    assert parent_identifiers == [
        ("parent1",),
        ("parent2",),
    ]


def test_supports_all_filters():
    """
    All FilterSchemaType values defined in the enum are correctly parsed and supported
    in our build_filter method.

    """
    for filter_type in FilterTypeEnum:
        # Mock FilterSchemaType
        mock_filter = MagicMock()
        value = (
            ["mock_name"]
            if filter_type in {FilterTypeEnum.IN, FilterTypeEnum.NOT_IN}
            else "mock_name"
        )
        mock_filter.dict.return_value = {f"name__{filter_type.value}": value}

        # Mock Query
        mock_query = MagicMock(spec=Query)

        store = StoreFilterMixin[SampleModel, SampleSchemaFilter](SampleModel)
        assert (
            store.build_filter(mock_query, mock_filter, include_archived=True)
            is not None
        )
