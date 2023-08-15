import pytest
from sqlalchemy.orm import Session

from lassen.queries import chain_select
from lassen.tests.model_fixtures import (
    SampleChainedChild,
    SampleChainedParent,
)


@pytest.fixture
def use_fixture_models(db_session: Session):
    if not db_session.bind:
        raise ValueError("No database connection")

    from lassen.db.base_class import Base

    Base.metadata.create_all(bind=db_session.bind)


def get_sql_representation(query):
    """
    Converting lists of SQLAlchemy objects to strings will return their memory-address
    but we want to compare to something nearer to the actual SQL representation.

    This function converts SQLAlchemy objects to strings in a way that is closer to a
    repr() of the SQL representation.

    """
    if isinstance(query, list):
        return [get_sql_representation(x) for x in query]
    elif isinstance(query, tuple):
        return tuple([get_sql_representation(x) for x in query])
    return str(query)


def test_single_join(use_fixture_models):
    x = chain_select(SampleChainedChild.parent)(SampleChainedParent.identifier)
    assert len(x.joins) == 1

    assert get_sql_representation(x.implicit_query_elements) == [
        "SampleChainedChild.parent_id",
        "aliased(SampleChainedParent).id",
    ]
    assert get_sql_representation(x.explicit_query_elements) == [
        "aliased(SampleChainedParent).identifier",
    ]
    assert get_sql_representation(x.joins) == [
        (
            "aliased(SampleChainedParent)",
            "samplechainedchild.parent_id = samplechainedparent_1.id",
        )
    ]


def test_multiple_joins(use_fixture_models):
    x = chain_select(SampleChainedChild.parent)(SampleChainedParent.parent)(
        SampleChainedParent.identifier
    )
    assert len(x.joins) == 2

    assert get_sql_representation(x.implicit_query_elements) == [
        "SampleChainedChild.parent_id",
        "aliased(SampleChainedParent).id",
        "aliased(SampleChainedParent).parent_id",
        "aliased(SampleChainedParent).id",
    ]
    assert get_sql_representation(x.explicit_query_elements) == [
        "aliased(SampleChainedParent).identifier",
    ]
    assert get_sql_representation(x.joins) == [
        (
            "aliased(SampleChainedParent)",
            "samplechainedchild.parent_id = samplechainedparent_1.id",
        ),
        (
            "aliased(SampleChainedParent)",
            "samplechainedparent.parent_id = samplechainedparent_1.id",
        ),
    ]

    # Assert that the aliases are actually different in memory
    assert x.joins[0][0] != x.joins[1][0]
