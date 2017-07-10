"""Turns an AST into a template structure.

This module implements the template system's semantic analyser and template
structure generator.  The end result is a tree-like template structure as
defined in (TODO: ref here) template.py.  It is reccomended that these methods
not be used directly by most common users, as the __init__.py file in this
directory contains convenient helper functions that shorten common template
generation operations to a single function call.
"""

from spade.template import template

TEMPLATE_ENTRY = "FILE"


class TemplateGeneratorException(Exception):
    """Raised when an issue is encountered processing a template AST."""

    pass


def _process_struct(target_file, struct_decl, struct=None, root=None,
        parent=None):
    """Process struct."""
    # Create the struct node if it wasn't given
    if not struct:
        struct = template.TStruct()

    # Process each field
    for field in struct_decl.fields:
        if isinstance(field, ast.AstStructValueField):
            pass # TODO: implement (we need to figure out if this is a struct or a static type)
        if isinstance(field, ast.AstStructArrayField):
            pass # TODO: implement
        else:
            raise TemplateGeneratorException(
                    "Bad field type: \"{}\"".format(type(field)))

def _process_root(target_file, ast):
    """Process the root struct declaration."""
    # Locate the entrypoint structure
    entry_struct_decl = ast_root.find_symbol(TEMPLATE_ENTRY)
    if not entry_struct_decl:
        raise TemplateGeneratorException("Template entry point not found.")

    # Process root like a struct, since it basically is one kinda
    root = template.TRoot()
    return _process_struct(target_file, struct_decl, root, root)

def generate_template(target_file, ast_root):
    """Generates a template given its AST and a target file to pull data from.

    :param target_file: Opened file the template should be applied to.
    :param ast_root: AstRoot object of the AST to parse.
    """
    # TODO: perform argument sanity checking

    return _process_root(target_file, ast_root)
