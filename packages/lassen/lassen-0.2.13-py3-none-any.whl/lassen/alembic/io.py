import importlib
import os
from inspect import isclass
from pathlib import Path

from lassen.db.base_class import Base
from lassen.io import guess_package_location


def guess_package_name():
    """
    Traverse the current path up to root and look for a pyproject.toml file.
    Once found, search for a migrate directory in its main directories.

    """
    package_path = guess_package_location("migrations")

    # Return the directory name, which is the name of the package
    return package_path.name


def get_migration_path(package_name: str):
    """
    By convention, client apps store their migrations in a sub-folder
    called `{package_name}.migrations`.
    """
    package = importlib.import_module(package_name)
    path = package.__path__

    migration_path = Path(path[0]) / "migrations"
    if not migration_path.exists():
        raise Exception(
            f"Could not find migrations folder at `{migration_path}`."
            " Did you forget to create it?"
        )

    return migration_path


def iterate_regular_package_files(
    package_name: str, exclude_patterns: list | None = None
):
    """
    Iterates over all files in a package, yielding the full module name of each file.

    """
    package = importlib.import_module(package_name)
    path = package.__path__

    for root, _, files in os.walk(path[0]):
        for file in files:
            if file.endswith(".py"):
                module_path = (Path(root) / file).relative_to(path[0])
                module_path = module_path.with_suffix("")
                module_formatted = str(module_path).replace("/", ".")

                module_elements = module_formatted.split(".")
                module_elements = [
                    part for part in module_elements if part != "__init__"
                ]
                module_elements = [package_name] + module_elements

                module_full = ".".join(module_elements)
                if exclude_patterns:
                    should_skip = any(
                        [f".{pattern}" in module_full for pattern in exclude_patterns]
                    )
                    if should_skip:
                        continue

                yield module_full


def get_sqlalchemy_base_subclasses(package_name: str):
    """
    Find all of the SQLAlchemy Model definitions that are contained in a package.
    Excludes test files since users typically don't want to create these in a migration.

    """
    for full_module_name in iterate_regular_package_files(
        package_name, ["test", "migrations"]
    ):
        module = importlib.import_module(full_module_name)

        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if isclass(attribute) and issubclass(attribute, Base) and attribute != Base:
                yield attribute
