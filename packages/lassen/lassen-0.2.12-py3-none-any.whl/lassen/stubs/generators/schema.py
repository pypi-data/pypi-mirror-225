import inspect
import types
import typing
from typing import Any, Callable, Type, get_args, get_origin

from jinja2 import Environment, FileSystemLoader, select_autoescape

from lassen.enums import FilterTypeEnum
from lassen.stubs.base import BaseGenerator, BaseStub, RenderedFile
from lassen.stubs.field import UNSET_VALUE, FieldDefinition
from lassen.stubs.generators.common import (
    ExtractedStubImports,
    extract_type_hints,
    format_dict_as_kwargs,
    format_typehint_as_string,
    get_ordered_instance_variables,
)
from lassen.stubs.templates import get_template_path


def is_optional(type_hint):
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    if origin is typing.Union or origin == types.UnionType:  # noqa E721
        return any(arg is type(None) for arg in args)
    elif isinstance(type_hint, type):
        return type_hint is type(None)
    return False


def make_optional(type_hint):
    if is_optional(type_hint):
        # The type hint is already Optional
        return type_hint
    else:
        origin = get_origin(type_hint)
        args = get_args(type_hint)

        if origin is typing.Union or origin == types.UnionType:  # noqa E721
            # Convert the Union to Optional by adding None as an argument
            return typing.Union[*args, type(None)]
        else:
            # If the type hint is not a Union, make it Optional
            return typing.Optional[type_hint]


class SchemaGenerator(BaseGenerator):
    def __call__(
        self,
        model: Type[BaseStub],
        import_hints: ExtractedStubImports,
    ):
        model_name = model.__name__

        # We use the same base schema but make some configuration choices based on
        # the majority of situations where these tend to be used:
        # 1. Updates are PATCH-like requests so we should allow None values across
        #   the board
        # 2. Read requests should be reading from an underlying data object, and
        #   therefore shouldn't have any default values
        create_fields, create_deps = self.get_model_fields(model, lambda f: f.create)
        update_fields, update_deps = self.get_model_fields(
            model, lambda f: f.update, force_optional=True
        )
        read_fields, read_deps = self.get_model_fields(
            model, lambda f: f.read, include_defaults=False
        )
        filter_fields, filter_deps = self.get_model_fields(
            model,
            lambda f: f.filter or not isinstance(f.filter_extensions, UNSET_VALUE),
            force_optional=True,
        )
        augmented_filters, augmented_deps = self.get_augmented_filter_fields(model)

        all_dependencies = set(
            create_deps + update_deps + read_deps + filter_deps + augmented_deps
        )

        # Set up Jinja2 environment
        env = Environment(
            loader=FileSystemLoader(get_template_path("")),
            autoescape=select_autoescape(["html", "xml"]),
        )

        template = env.get_template("schema.py.j2")
        content = template.render(
            model_name=model_name,
            create_fields=create_fields,
            update_fields=update_fields,
            read_fields=read_fields,
            filter_fields=filter_fields + augmented_filters,
            dependencies=sorted(
                [dependency for dependency in all_dependencies if dependency]
            ),
            clone_imports=import_hints.clone_imports,
            clone_typechecking_imports=import_hints.clone_typechecking_imports,
        )

        return RenderedFile(
            content=content,
            created_classes=[
                model_name,
                f"{model_name}Create",
                f"{model_name}Update",
                f"{model_name}Filter",
                f"{model_name}Base",
            ],
        )

    def get_model_fields(
        self,
        model: Type[BaseStub],
        field_predicate: Callable[[FieldDefinition], bool] | None = None,
        force_optional: bool = False,
        include_defaults: bool = True,
    ):
        fields: list[tuple[str, FieldDefinition]] = list(
            inspect.getmembers(
                model,
                lambda m: isinstance(m, FieldDefinition)
                and (not field_predicate or field_predicate(m)),
            )
        )

        fields_ordered = get_ordered_instance_variables(model)
        fields = sorted(fields, key=lambda f: fields_ordered.index(f[0]))

        declarations: list[str] = []
        dependencies: set[str | None] = set()
        typehints = extract_type_hints(model, FieldDefinition)

        for name, field in fields:
            # Determine if this generator should process this field
            if field.generators is not None:
                if self not in field.generators:
                    continue

            typehint = typehints[name]
            if force_optional:
                typehint = make_optional(typehint)

            mapped_typehint, type_dependencies = format_typehint_as_string(typehint)

            declaration = f"{name}: {mapped_typehint}"
            field_arguments: dict[str, Any] = {}
            if include_defaults:
                if force_optional:
                    field_arguments["default"] = None
                elif not isinstance(field.default, UNSET_VALUE):
                    if callable(field.default):
                        field_arguments["default_factory"] = field.default
                    else:
                        field_arguments["default"] = field.default
                elif is_optional(typehint):
                    # Default typehint is optional, so we should set the default to None
                    # so users don't have to manually set it
                    field_arguments["default"] = None

            if field.description:
                field_arguments["description"] = field.description

            if field.examples:
                field_arguments["examples"] = field.examples

            if field_arguments:
                declaration += f" = Field({format_dict_as_kwargs(field_arguments)})"
            declarations.append(declaration)
            dependencies |= set(type_dependencies)

        if not declarations:
            declarations.append("pass")

        return declarations, list(dependencies)

    def get_augmented_filter_fields(self, model: Type[BaseStub]):
        """
        Format field filters, like `id__in` or `value__not`

        These have a different syntax pattern than our other fields, which are
        1:1 to the declaration name.

        """
        filter_fields: list[tuple[str, FieldDefinition]] = list(
            inspect.getmembers(model, lambda m: isinstance(m, FieldDefinition))
        )

        fields_ordered = get_ordered_instance_variables(model)
        filter_fields = sorted(filter_fields, key=lambda f: fields_ordered.index(f[0]))

        typehints = extract_type_hints(model, FieldDefinition)

        declarations: list[str] = []
        dependencies: set[str | None] = set()

        for name, field in filter_fields:
            # Determine if this generator should process this field
            if field.generators is not None:
                if self not in field.generators:
                    continue

            if isinstance(field.filter_extensions, UNSET_VALUE):
                continue

            typehint = typehints[name]

            for filter_extension in field.filter_extensions:
                if filter_extension == FilterTypeEnum.IN:
                    typehint = make_optional(typing.List[typehint])  # type: ignore
                elif filter_extension == FilterTypeEnum.NOT_IN:
                    typehint = make_optional(typing.List[typehint])  # type: ignore
                else:
                    typehint = make_optional(typehint)

                mapped_typehint, type_dependencies = format_typehint_as_string(typehint)

                declaration = f"{name}__{filter_extension.value}: {mapped_typehint}"
                field_arguments: dict[str, Any] = {
                    "default": None,
                }
                if field.description:
                    field_arguments["description"] = field.description

                if field_arguments:
                    declaration += f" = Field({format_dict_as_kwargs(field_arguments)})"

                declarations.append(declaration)
                dependencies |= set(type_dependencies)

        return declarations, list(dependencies)
