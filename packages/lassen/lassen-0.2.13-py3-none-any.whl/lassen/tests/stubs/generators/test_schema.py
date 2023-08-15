from typing import Dict, List, Optional, Union

import pytest

from lassen.stubs.generators.schema import is_optional, make_optional


@pytest.mark.parametrize(
    "input_type, expected_output",
    [
        (int, Union[int, type(None)]),
        (int, int | None),
        (str | int, Union[str, int, type(None)]),
        (str, Union[str, type(None)]),
        (List[int], Union[List[int], type(None)]),
        (Dict[str, int], Union[Dict[str, int], type(None)]),
        (Union[int, str], Union[int, str, type(None)]),
        (Union[int, None], Union[int, None]),
        (Optional[int], Union[int, None]),
        (Optional[str], Union[str, None]),
    ],
)
def test_make_optional(input_type, expected_output):
    assert make_optional(input_type) == expected_output


@pytest.mark.parametrize(
    "input_type, expected_output",
    [
        (int, False),
        (str, False),
        (List[int], False),
        (Dict[str, int], False),
        (Union[int, str], False),
        (Union[int, None], True),
        (Optional[int], True),
        (Optional[str], True),
        (str | None, True),
    ],
)
def test_is_optional(input_type, expected_output):
    assert is_optional(input_type) == expected_output
