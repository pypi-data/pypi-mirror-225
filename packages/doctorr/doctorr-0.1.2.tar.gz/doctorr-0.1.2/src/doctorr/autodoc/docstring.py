import re
from dataclasses import dataclass, field, fields
from functools import singledispatch
from itertools import zip_longest
from textwrap import dedent
from typing import ClassVar, List, Optional, Union

from doctorr.autodoc.inspection import (
    InspectedClass,
    InspectedFunction,
    InspectedMethod,
    InspectedPage,
    InspectedProperty,
)

# note  docstring is a bad name for this module.
#       it does more than handling docstring


@dataclass
class Field:
    name: str
    type: Optional[str]
    text: str


@dataclass
class Docstring:
    description: str = ""
    attributes: List[Field] = field(default_factory=list)
    args: List[Field] = field(default_factory=list)
    returns: List[Field] = field(default_factory=list)
    yields: List[Field] = field(default_factory=list)
    raises: List[Field] = field(default_factory=list)

    @property
    def sections(self):
        return [
            {
                "title": Docstring.MAP_SECTION_NAME_TO_TITLE[f.name],
                "fields": getattr(self, f.name),
            }
            for f in fields(self)
            if f.name != "description"
        ]

    MAP_SECTION_NAME_TO_TITLE: ClassVar = {
        "attributes": "Attributes",
        "args": "Parameters",
        "returns": "Returns",
        "yields": "Yields",
        "raises": "Raises",
    }


@dataclass
class ProcessedFunction:
    name: str
    signature: str
    docstring: Docstring


@dataclass
class ProcessedMethod:
    name: str
    signature: str
    docstring: Docstring


@dataclass
class ProcessedProperty:
    name: str
    docstring: Docstring


@dataclass
class ProcessedClass:
    name: str
    docstring: Docstring
    members: List[Union[ProcessedMethod, ProcessedProperty]]
    signature: str = "()"


@dataclass
class ProcessedPage:
    title: str
    output_name: str
    module_source: str
    docstring: Docstring
    content: List[Union[ProcessedClass, ProcessedFunction]]

    @property
    def name(self):
        return self.title


def parse_google_docstring(docstring: str) -> Docstring:
    if not docstring:
        return Docstring()  # empty docstring
    sections = _split_into_sections(docstring)
    description = _dedent_description(sections.get("Description", ""))
    args = _parse_fields_section(sections.get("Parameters", ""))
    returns = _parse_fields_section(sections.get("Returns", ""))
    yields = _parse_fields_section(sections.get("Yields", ""))
    raises = _parse_fields_section(sections.get("Raises", ""))
    attributes = _parse_fields_section(sections.get("Attributes", ""))
    return Docstring(description, attributes, args, returns, yields, raises)


def _dedent_description(description):
    """Remove common leading whitespace from every line in the given description.

    This function is designed to handle typical Python docstrings, where the first line
    of the docstring might be on the same line as the opening triple quotes, followed by
    a newline, and subsequent lines may have a common indentation level.
    """
    if not description:
        return ""
    # the first line of a docstring maybe indented differenly than the rest
    first_line, *rest = description.split("\n")
    first_line = first_line.strip()
    rest = dedent("\n".join(rest))
    return "\n".join([first_line, rest])


SECTION_REGEX = re.compile(
    r"^\s*(Args:|Arguments:|Parameters:|Returns:|Return:|Raises:|Yields:|"
    "Attributes:)",
    re.MULTILINE,
)

# This is used to map aliases toward the unique sections
SECTION_MAP = {
    "Args:": "Parameters",
    "Arguments:": "Parameters",
    "Parameters:": "Parameters",
    "Returns:": "Returns",
    "Return:": "Returns",
    "Raises:": "Raises",
    "Yields:": "Yields",
    "Attributes:": "Attributes",
    "Description": "Description",  # no : because it's a field we are creating
}


def _identify_function_intervals(docstring):
    """Identify where the sections starts and end as well as their title.

    Returns a list of dict with keys {"title", "start", "end"}.

    Warning: "start" and "end" are the indexes in the full docstring
    (not the line numbers)
    """
    matches = list(SECTION_REGEX.finditer(docstring))
    sections = [{"start": m.start(), "title": m.group(0).strip()} for m in matches]
    sections.insert(0, {"start": 0, "title": "Description"})
    sections = [
        {**section, "end": next_["start"]}
        for section, next_ in zip_longest(
            sections, sections[1:], fillvalue={"start": None}
        )
    ]
    return sections


def _check_for_duplicate_sections(sections):
    if len(set([SECTION_MAP[s["title"]] for s in sections])) < len(sections):
        raise ValueError("Duplicate section detected.")


def _split_into_sections(docstring: str) -> dict:
    sections = _identify_function_intervals(docstring)
    _check_for_duplicate_sections(sections)
    return {
        SECTION_MAP[section["title"]]: docstring[section["start"] : section["end"]]
        for section in sections
    }


_field_parens_regex = re.compile(r"\s*(\w+)\s*\(\s*(.+?)\s*\)")


def _parse_fields_section(section_text: str) -> List[Field]:
    fields = []
    lines = section_text.strip().split("\n")
    lines = lines[1:]  # skip section title

    for line in lines:
        if ":" in line:
            _name, _, _desc = line.partition(":")
            _name, _type, _desc = _name.strip(), "", _desc.strip()
            match = _field_parens_regex.match(_name)
            if match:
                _name = match.group(1)
                _type = match.group(2)
            fields.append(Field(name=_name, type=_type, text=_desc.strip()))
        elif fields:
            # This is a continuation of the description of the previous field
            fields[-1].text += " " + line.strip()

    return fields


@singledispatch
def process_inspected_item(item):
    raise NotImplementedError(f"Cannot handle {type(item)}")


@process_inspected_item.register(InspectedFunction)
def _(item: InspectedFunction):
    doc = parse_google_docstring(item.docstring)
    return ProcessedFunction(name=item.name, signature=item.signature, docstring=doc)


@process_inspected_item.register(InspectedClass)
def _(item: InspectedClass):
    class_doc = parse_google_docstring(item.docstring)
    processed_members = []
    for member in item.members:
        processed_member = process_inspected_item(member)
        if processed_member:
            processed_members.append(processed_member)
    return ProcessedClass(
        name=item.name,
        signature=item.init_signature,
        docstring=class_doc,
        members=processed_members,
    )


@process_inspected_item.register(InspectedMethod)
def _(item: InspectedMethod):
    doc = parse_google_docstring(item.docstring)
    return ProcessedMethod(name=item.name, signature=item.signature, docstring=doc)


@process_inspected_item.register(InspectedProperty)
def _(item: InspectedProperty):
    doc = parse_google_docstring(item.docstring)
    return ProcessedProperty(name=item.name, docstring=doc)


def process_page(inspected_page: InspectedPage) -> ProcessedPage:
    processed_content = [
        process_inspected_item(item) for item in inspected_page.content
    ]
    module_doc = parse_google_docstring(inspected_page.module_docstring)

    return ProcessedPage(
        title=inspected_page.title,
        output_name=inspected_page.output_name,
        module_source=inspected_page.module_source,
        docstring=module_doc,
        content=processed_content,
    )
