from functools import singledispatch

from doctorr.autodoc.docstring import (
    ProcessedClass,
    ProcessedFunction,
    ProcessedMethod,
    ProcessedPage,
    ProcessedProperty,
)


@singledispatch
def _render_element(processed_element, template_renderer) -> str:
    raise ValueError(f"Unsupported ProcessedElement type: {type(processed_element)}")


def element_to_template_dict(processed_element):
    return {
        "name": processed_element.name,
        "signature": getattr(processed_element, "signature", ""),
        "docstring": processed_element.docstring,
    }


@_render_element.register(ProcessedClass)
def _(processed_element, renderer) -> str:
    context = element_to_template_dict(processed_element)
    template_name = "class.jinja2"
    rendered_members = [
        _render_element(member, renderer) for member in processed_element.members
    ]
    context["rendered_members"] = "".join(rendered_members)
    return renderer.render(template_name, context)


@_render_element.register(ProcessedFunction)
def _(processed_element, renderer) -> str:
    context = element_to_template_dict(processed_element)
    template_name = "function.jinja2"
    return renderer.render(template_name, context)


@_render_element.register(ProcessedMethod)
def _(processed_element, renderer) -> str:
    context = element_to_template_dict(processed_element)
    template_name = "method.jinja2"
    return renderer.render(template_name, context)


@_render_element.register(ProcessedProperty)
def _(processed_element, renderer) -> str:
    context = element_to_template_dict(processed_element)
    template_name = "property.jinja2"
    return renderer.render(template_name, context)


@_render_element.register(ProcessedPage)
def _(processed_element, renderer) -> str:
    context = element_to_template_dict(processed_element)
    template_name = "page.jinja2"
    rendered_content = [
        _render_element(piece_of_content, renderer)
        for piece_of_content in processed_element.content
    ]
    context["rendered_content"] = "".join(rendered_content)
    return renderer.render(template_name, context)


def render_page(page, renderer):
    return _render_element(page, renderer)
