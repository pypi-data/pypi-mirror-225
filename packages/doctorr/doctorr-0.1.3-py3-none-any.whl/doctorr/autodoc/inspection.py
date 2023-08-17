import inspect
import sys
from dataclasses import dataclass
from functools import singledispatch
from importlib import import_module
from typing import List, Optional, Union

from doctorr.autodoc.parse_config import (
    ClassEntry,
    FunctionEntry,
    MethodEntry,
    PageConfig,
    PropertyEntry,
)


@dataclass
class InspectedProperty:
    name: str
    docstring: Optional[str]


@dataclass
class InspectedMethod:
    name: str
    signature: str
    docstring: Optional[str]


@dataclass
class InspectedFunction:
    name: str
    signature: str
    docstring: Optional[str]


@dataclass
class InspectedClass:
    name: str
    init_signature: Optional[str]
    docstring: Optional[str]
    members: List[Union[InspectedMethod, InspectedProperty]]


@dataclass
class InspectedPage:
    title: str
    output_name: str
    module_source: str
    module_docstring: Optional[str]
    content: List[Union[InspectedClass, InspectedFunction]]


@singledispatch
def inspect_entry(entry, parent):
    raise NotImplementedError(f"Cannot handle {type(entry)}")


@inspect_entry.register(FunctionEntry)
def _(entry: FunctionEntry, parent):
    func = getattr(parent, entry.name, None)
    if func and callable(func):
        signature = str(inspect.signature(func))
        return InspectedFunction(
            name=func.__name__, signature=signature, docstring=func.__doc__
        )


@inspect_entry.register(ClassEntry)
def _(entry: ClassEntry, parent):
    cls = getattr(parent, entry.name, None)
    if not cls:
        raise AttributeError(entry.name)

    members = []
    for member_config in entry.members:
        extracted_member = inspect_entry(member_config, cls)
        if extracted_member:
            members.append(extracted_member)

    init_signature = None
    if hasattr(cls, "__init__"):
        init_signature = (
            str(inspect.signature(cls.__init__))
            .replace("(self, ", "(")
            .replace("(self)", "()")
        )

    return InspectedClass(
        name=cls.__name__,
        init_signature=init_signature,
        docstring=cls.__doc__,
        members=members,
    )


@inspect_entry.register(MethodEntry)
def _(entry: MethodEntry, parent):
    method = getattr(parent, entry.name, None)
    if method and callable(method):
        signature = str(inspect.signature(method))
        return InspectedMethod(
            name=method.__name__, signature=signature, docstring=method.__doc__
        )


@inspect_entry.register(PropertyEntry)
def _(entry: PropertyEntry, parent):
    prop = getattr(parent, entry.name, None)
    if isinstance(prop, property):
        return InspectedProperty(name=prop.fget.__name__, docstring=prop.__doc__)


def import_and_inspect(page_config: PageConfig, watch: bool) -> InspectedPage:
    module_name = page_config.module_source
    # hot module reload
    if watch and module_name in sys.modules:
        del sys.modules[module_name]

    module = import_module(module_name)
    module_docstring = module.__doc__ if page_config.include_module_docstring else None

    content_list = []
    for item in page_config.content:
        content_item = inspect_entry(item, module)
        if content_item:
            content_list.append(content_item)

    return InspectedPage(
        title=page_config.title,
        output_name=page_config.output_name,
        module_source=page_config.module_source,
        module_docstring=module_docstring,
        content=content_list,
    )
