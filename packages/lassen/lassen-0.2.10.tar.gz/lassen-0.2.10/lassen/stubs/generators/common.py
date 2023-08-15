import ast
import builtins
import enum
import inspect
import types
import typing
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, get_args, get_origin

import pydantic

from lassen.stubs.base import BaseStub


def format_import(cls):
    # Get module of the class
    module = inspect.getmodule(cls)

    if isinstance(cls, typing.ForwardRef):
        return None

    if module is None or module.__name__ == "__main__":
        raise ValueError(f"{cls} is not part of a module.")

    module_name = module.__name__
    class_name = cls.__name__
    if module == builtins:
        return None
    return f"from {module_name} import {class_name}"


def extract_type_hints(cls, required_superclass: type):
    """
    :param required_superclass: Only extract type hints from fields that are instances
        of the given class. Useful to limit typehints to only Field instances
        or Generator instances.
    """
    if not issubclass(cls, BaseStub):
        raise ValueError("cls must be a subclass of BaseStub")

    # Explicitly don't resolve forward references (unlike typing.get_type_hints(cls))
    # to avoid possible circular dependencies
    type_hints = cls.__annotations__
    for parent in cls.__bases__:
        type_hints = {
            **parent.__annotations__,
            **type_hints,
        }

    fields = {}
    for name, type_hint in type_hints.items():
        if isinstance(getattr(cls, name), required_superclass):
            fields[name] = type_hint

    return fields


def format_typehint_as_string(typehint) -> tuple[str, list[str]]:
    """
    Prepare a generic typehint for string insertion into a template as a hint value

    Effectively just takes the runtime value of a typehint and converts it back into the
    code that creates that typehint

    """
    origin = get_origin(typehint)
    args = get_args(typehint)

    # Handle case for NoneType
    if typehint is type(None):
        return "None", []

    # Handle case for Unions, which might represent nullable fields
    if origin is typing.Union or origin == types.UnionType:  # noqa E721
        union_args = ", ".join([format_typehint_as_string(t)[0] for t in args])
        return f"Union[{union_args}]", [format_import(t) for t in args] + [
            format_import(typing.Union)
        ]

    # Handle case for Enum
    if isinstance(typehint, enum.EnumMeta):
        return typehint.__name__, [format_import(typehint)]

    # Handle case for built-in types
    if origin is None and not args:
        if isinstance(typehint, str):
            # Forward reference, we assume dependencies are taken care of with the
            # standard import pipline
            return f"'{typehint}'", []
        elif isinstance(typehint, typing.ForwardRef):
            return f"'{typehint.__forward_arg__}'", []
        elif (
            inspect.isclass(typehint)
            and issubclass(typehint, pydantic.BaseModel)
            and not issubclass(typehint, BaseStub)
        ):
            # Support non-stub pydantic schemas
            return f"{typehint.__name__}", [format_import(typehint)]
        else:
            return typehint.__name__, [format_import(typehint)]

    # Handle case for generic types like List, Dict
    if origin is not None or args:
        if origin:
            typehint_name = origin.__name__
        else:
            typehint_name = typehint.__name__

        arg_names: list[str] = []
        arg_deps: list[str] = []

        for arg in args:
            arg_name, arg_dep = format_typehint_as_string(arg)
            arg_names.append(arg_name)
            arg_deps.extend(arg_dep)

        arg_types = ", ".join(arg_names)
        return f"{typehint_name}[{arg_types}]", arg_deps

    raise NotImplementedError(f"Type hint {typehint} not supported")


def is_lambda(v):
    LAMBDA = lambda: 0  # noqa

    return isinstance(v, type(LAMBDA)) and v.__name__ == LAMBDA.__name__


def get_lambda_body(func: Callable) -> str:
    func_lines, start_number = inspect.getsourcelines(func)
    func_range = set(range(start_number, start_number + len(func_lines)))

    file_path = inspect.getsourcefile(func)
    if not file_path:
        raise ValueError("Could not find source file for provided lambda.")
    with open(file_path, "r") as file:
        file_content = file.read()
    module = ast.parse(file_content)

    found_lambds: list[Any] = []
    todo: Any = deque([module])

    while todo:
        node = todo.popleft()
        # Only consider the outermost Lambda function, in the case of nested functions
        if isinstance(node, ast.Lambda):
            if node.lineno in func_range:
                found_lambds.append(node)
        else:
            todo.extend(ast.iter_child_nodes(node))

    if found_lambds:
        if len(found_lambds) > 1:
            raise ValueError(
                f"Multiple lambda functions found on the same line: {func_lines}"
            )
        return ast.unparse(found_lambds[0].body).strip()

    raise ValueError("No lambda function found in provided function.")


def format_dict_as_kwargs(dictionary: dict[str, Any]):
    """
    Formats a dictionary as keyword arguments. If a dictionary value is
    a lambda function, will attempt to extract its value as a string.

    """
    # These representations can be explicitly cast
    # Everything else should be in a lambda
    allowed_representations = (str, int, float, bool, type(None))
    representation_dict: dict[str, str] = {}

    def convert_value(value: Any):
        if isinstance(value, enum.Enum):
            return f"{value.__class__.__name__}.{value.name}"
        elif is_lambda(value):
            return f"lambda: {get_lambda_body(value)}"
        elif isinstance(value, list):
            # Convert the args
            converted_args: list[str] = [convert_value(arg) for arg in value]
            return f"[{', '.join(converted_args)}]"
        elif isinstance(value, allowed_representations):
            # Allowed representation fallback should be the last in the chain, since
            # these classes might be superclasses of other more specific targeting
            # (StrEnum, for instance) that we would rather process by their
            # targeted handler
            return repr(value)
        else:
            raise ValueError(
                f"Value {value} is not a valid default; cast with `lambda` in your"
                " code to maintain its representation."
            )

    for key, value in dictionary.items():
        representation_dict[key] = convert_value(value)

    return ", ".join(f"{k}={v}" for k, v in representation_dict.items())


def get_ordered_instance_variables(model: type):
    fields_ordered: list[str] = []

    # Recursively gather variables from the parent classes
    for parent in model.__bases__:
        fields_ordered.extend(get_ordered_instance_variables(parent))

    # Fetch the variables from the model's class itself
    model_vars = [key for key in vars(model).keys() if not key.startswith("__")]
    fields_ordered.extend(model_vars)

    return fields_ordered


@dataclass
class ImportDefinition:
    definition: str
    is_typechecking: bool = False


@dataclass
class ExtractedStubImports:
    clone_imports: list[str]
    clone_typechecking_imports: list[str]


def extract_stub_imports(path: Path | list[Path]):
    """
    Given a path, extract the import statements from its source file.

    This is used to clone imports from the original stub file in case they capture
    typehints that are not explicitly used in the model

    """
    if not isinstance(path, list):
        paths = [path]
    else:
        paths = path

    stub_imports: list[ImportDefinition] = []

    for path in paths:
        with open(path, "r") as file:
            file_content = file.read()
        module = ast.parse(file_content)

        # Ignore lassen imports by default, since this often brings in conflicting
        # type definitions
        stub_imports += [
            module_import
            for module_import in extract_imports(module)
            if "lassen" not in module_import.definition
        ]

    return ExtractedStubImports(
        clone_imports=[
            import_def.definition
            for import_def in stub_imports
            if not import_def.is_typechecking
        ],
        clone_typechecking_imports=[
            import_def.definition
            for import_def in stub_imports
            if import_def.is_typechecking
        ],
    )


def extract_imports(
    node: Any, under_type_checking: bool = False
) -> Iterable[ImportDefinition]:
    if isinstance(node, ast.Import):
        definition = f"import {','.join([alias.name for alias in node.names])}"
        yield ImportDefinition(
            definition=definition, is_typechecking=under_type_checking
        )
        return
    elif isinstance(node, ast.ImportFrom):
        imported_objects = ", ".join([alias.name for alias in node.names])
        level_dots = "." * node.level if node.level > 0 else ""
        definition = f"from {level_dots}{node.module} import {imported_objects}"
        yield ImportDefinition(
            definition=definition, is_typechecking=under_type_checking
        )
        return
    elif (
        isinstance(node, ast.If)
        and isinstance(node.test, ast.Name)
        and node.test.id == "TYPE_CHECKING"
    ):
        for sub_node in node.body:
            yield from extract_imports(sub_node, True)
    else:
        for sub_node in ast.iter_child_nodes(node):  # type: ignore
            yield from extract_imports(sub_node, under_type_checking)
