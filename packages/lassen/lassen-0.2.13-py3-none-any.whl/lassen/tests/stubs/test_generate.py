import shutil
from os import chdir, getcwd
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from lassen.stubs.generate import generate_files
from lassen.tests.fixtures import get_fixture_path


@pytest.fixture
def temp_project():
    with TemporaryDirectory() as temp_project:
        project_path = Path(temp_project)

        (project_path / "test_project").mkdir()
        (project_path / "test_project" / "stubs").mkdir()

        with open(project_path / "pyproject.toml", "w") as file:
            file.write("N/A")
        with open(project_path / "test_project" / "__init__.py", "w") as file:
            file.write("")
        with open(project_path / "test_project" / "stubs" / "__init__.py", "w") as file:
            file.write("")

        # Copy in our programatic fixtures
        shutil.copy(
            get_fixture_path("stubs/fixtures.py"),
            project_path / "test_project" / "stubs",
        )

        current_path = getcwd()
        chdir(project_path)
        try:
            yield project_path
        finally:
            chdir(current_path)


def test_generator(temp_project: Path):
    def format_import(model):
        return f"from MOCKED_PACKAGE import {model.__name__}"

    # Since we don't actually install the package, the import introspection will fail
    with patch("lassen.stubs.generators.common.format_import") as mocked_import:
        mocked_import.side_effect = format_import
        generate_files()

    store_files = [
        path.name for path in (temp_project / "test_project" / "stores").iterdir()
    ]
    schema_files = [
        path.name for path in (temp_project / "test_project" / "schemas").iterdir()
    ]
    public_schema_files = [
        path.name
        for path in (temp_project / "test_project" / "schemas_public").iterdir()
    ]

    assert set(store_files) == {"__init__.py", "user_stub.py"}
    assert set(schema_files) == {"__init__.py", "user_stub.py"}
    assert set(public_schema_files) == {"__init__.py", "user_stub.py"}

    assert (
        temp_project / "test_project" / "stores" / "user_stub.py"
    ).read_text() == get_fixture_path("stubs/expected_store.py").read_text()

    assert (
        temp_project / "test_project" / "schemas" / "user_stub.py"
    ).read_text() == get_fixture_path("stubs/expected_schema.py").read_text()

    assert (
        temp_project / "test_project" / "schemas_public" / "user_stub.py"
    ).read_text() == get_fixture_path("stubs/expected_schema_public.py").read_text()
