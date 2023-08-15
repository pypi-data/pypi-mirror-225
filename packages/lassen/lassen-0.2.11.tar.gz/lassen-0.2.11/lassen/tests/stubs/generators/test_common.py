from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List

import pytest
from pydantic import BaseModel

from lassen.stubs.generators.common import (
    extract_stub_imports,
    format_dict_as_kwargs,
    format_typehint_as_string,
    get_lambda_body,
    get_ordered_instance_variables,
    is_lambda,
)
from lassen.tests.fixtures import get_fixture_path


class SimpleEnum(Enum):
    TEST = "TEST"


class SimplePydanticModel(BaseModel):
    TEST: str


@pytest.mark.parametrize(
    "typehint, expected",
    [
        (int, "int"),
        (float, "float"),
        (SimpleEnum, "SimpleEnum"),
        (list[str], "list[str]"),
        (str | None, "Union[str, None]"),
        (List[str], "list[str]"),
        (Dict[str, str], "dict[str, str]"),
        (dict[str, str], "dict[str, str]"),
        (SimplePydanticModel, "SimplePydanticModel"),
    ],
)
def test_format_typehint_as_string(typehint, expected):
    formatted_typehint, dependencies = format_typehint_as_string(typehint)
    assert formatted_typehint == expected
    assert len(dependencies) > 0


@pytest.mark.parametrize(
    "input_dict, expected_str",
    [
        ({"a": 1, "b": lambda: datetime.now()}, "a=1, b=lambda: datetime.now()"),
        ({"a": 1, "b": lambda: datetime.now}, "a=1, b=lambda: datetime.now"),
    ],
)
def test_format_dict_as_kwargs(input_dict: dict[str, Any], expected_str: str):
    assert format_dict_as_kwargs(input_dict) == expected_str


@pytest.mark.parametrize(
    "input_lambda, expected_str",
    [
        (lambda: 0, "0"),
        (lambda: "ABC", "'ABC'"),
        (lambda: datetime.now(), "datetime.now()"),
        (lambda: datetime.now, "datetime.now"),
        (lambda: lambda: datetime.now, "lambda: datetime.now"),
    ],
)
def test_get_lambda_body(input_lambda: Callable, expected_str: str):
    assert get_lambda_body(input_lambda) == expected_str


@pytest.mark.parametrize(
    "input_variable, expected_is_lambda",
    [
        (lambda: 0, True),
        (lambda: datetime.now(), True),
        (0, False),
    ],
)
def test_is_lambda(input_variable: Any, expected_is_lambda: bool):
    assert is_lambda(input_variable) == expected_is_lambda


@pytest.mark.parametrize(
    "model,expected_output",
    [
        # Case: a class with no parents
        (type("SimpleClass", (), {"a": 1, "b": 2}), ["a", "b"]),
        # Case: a class with one parent
        (
            type("ChildClass", (type("ParentClass", (), {"a": 1, "b": 2}),), {"c": 3}),
            ["a", "b", "c"],
        ),
        # Case: a class with multiple parents
        (
            type(
                "ChildClass",
                (
                    type("ParentClass1", (), {"a": 1, "b": 2}),
                    type("ParentClass2", (), {"x": 1, "y": 2}),
                ),
                {"z": 3},
            ),
            ["a", "b", "x", "y", "z"],
        ),
    ],
)
def test_get_ordered_instance_variables(model, expected_output):
    assert get_ordered_instance_variables(model) == expected_output


@pytest.mark.parametrize(
    "path, expected_headers, expected_typehints",
    [
        (
            get_fixture_path("stubs/fixtures.py"),
            [
                "from datetime import datetime",
                "from enum import Enum",
                "from typing import TYPE_CHECKING",
            ],
            [
                "from datetime import timezone",
            ],
        )
    ],
)
def test_extract_stub_imports(
    path: Path, expected_headers: list[str], expected_typehints: list[str]
):
    extracted_stubs = extract_stub_imports(path)
    assert extracted_stubs.clone_imports == expected_headers
    assert extracted_stubs.clone_typechecking_imports == expected_typehints
