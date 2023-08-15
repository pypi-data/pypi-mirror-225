import importlib
import importlib.util
import inspect
import os
import pkgutil
import sys
from pathlib import Path
from typing import Type

from click import command, secho
from inflection import underscore

from lassen.io import guess_package_location
from lassen.stubs.base import BaseGenerator, BaseStub
from lassen.stubs.generators.common import extract_stub_imports

CLIENT_STUB_DIRECTORY = "stubs"


def generate_files() -> list[Type[BaseStub]]:
    root_path = guess_package_location(CLIENT_STUB_DIRECTORY)
    sys.path.append(os.path.dirname(root_path))

    stub_models: list[tuple[Type[BaseStub], Path]] = []

    package = importlib.import_module(root_path.name)

    for _, module_name, _ in pkgutil.walk_packages(
        path=package.__path__, prefix=package.__name__ + "."
    ):
        # Speed up the search by skipping modules that are clearly not
        # in the stubs directory
        if CLIENT_STUB_DIRECTORY not in module_name:
            continue

        definition_module = importlib.import_module(module_name)

        stub_models += [
            (val, Path(inspect.getfile(val)))
            for _, val in inspect.getmembers(
                definition_module,
                lambda x: inspect.isclass(x) and issubclass(x, BaseStub),
            )
            if val != BaseStub
        ]

    if not stub_models:
        secho(f"No stub models found, checked: {root_path}", fg="red")
        return []

    secho("Found stub models:", fg="blue")
    for model, path in stub_models:
        secho(f"  {model.__name__} ({path.name})", fg="blue")

    model_generators: list[tuple[Type[BaseStub], Path, list[BaseGenerator]]] = [
        (
            model,
            path,
            [
                generator
                for _, generator in inspect.getmembers(
                    model, lambda m: isinstance(m, BaseGenerator)
                )
            ],
        )
        for model, path in stub_models
    ]

    unique_generators = set(
        generator for _, _, generators in model_generators for generator in generators
    )

    # Set up the base folders
    # This includes a new __init__ stub in each directory that can be
    # used to import dependency files
    for generator in unique_generators:
        generator_output = root_path / generator.output_directory
        generator_output.mkdir(parents=True, exist_ok=True)

        # Clear the old files, since the user might have deleted the
        # underlying stubs in the meantime
        for file in generator_output.iterdir():
            if file.is_file():
                file.unlink()

        with open(generator_output / "__init__.py", "w") as f:
            f.write("")

    try:
        for model, path, generators in model_generators:
            # Extract the explicit import from the model and its user-defined parents
            # Skip the lassen-internal base class itself since this won't have any
            # imports that are relevant to the definitions
            parent_paths = [
                Path(inspect.getfile(model))
                for model in model.__bases__
                if model != BaseStub
            ]
            stub_imports = extract_stub_imports([path] + parent_paths)

            secho(f"Generating files for {model.__name__}")

            for generator in generators:
                generator_output = root_path / generator.output_directory
                rendered = generator(model, import_hints=stub_imports)
                with open(
                    generator_output / f"{underscore(model.__name__)}.py", "w"
                ) as f:
                    f.write(rendered.content)

                with open(generator_output / "__init__.py", "a") as f:
                    formatted_class_names = ", ".join(rendered.created_classes)
                    f.write(
                        f"from .{underscore(model.__name__)}"
                        f" import {formatted_class_names} # noqa: 401\n"
                    )

            if generators:
                secho(f"Generated files for {model.__name__}", fg="green")
            else:
                secho(f"No generators found for {model.__name__}", fg="yellow")
    except Exception as e:
        secho("Exception encountered, cleaning up filesystem...", fg="red")

        for generator in unique_generators:
            generator_output = root_path / generator.output_directory
            generator_output.mkdir(parents=True, exist_ok=True)

            # Clear the old files, since the user might have deleted the underlying
            # stubs in the meantime
            for file in generator_output.iterdir():
                if file.is_file():
                    file.unlink()

            with open(generator_output / "__init__.py", "w") as f:
                f.write("")

        raise e

    return [model for model, _ in stub_models]


@command()
def cli():
    generate_files()
