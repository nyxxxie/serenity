"""Turns an AST into a template structure.

This module implements the template system's semantic analyser and template
structure generator.  The end result is a tree-like template structure as
defined in (TODO: ref here) template.py.  It is reccomended that these methods
not be used directly by most common users, as the __init__.py file in this
directory contains convenient helper functions that shorten common template
generation operations to a single function call.
"""

import logging
from spade.template import ast
from spade.template import template

TEMPLATE_ENTRY = "FILE"


class TemplateGeneratorException(Exception):
    """Raised when an issue is encountered processing a template AST."""

    pass


class TemplateGenerator(object):
    """."""

    def __init__(self, target_file, ast):
        self._target_file = target_file
        self._root = None
        self._ast = ast
        self.process_root()

    @property
    def root(self):
        return self._root

    def refresh():
        if self.root:
            self.root.refresh()

    def process_var(self, field_decl, parent=None):
        """Process var."""

        logging.debug("Processing var [type: \"{}\", name: \"{}\"]".format(
                field_decl.typename, field_decl.name))

        # Find type
        # TODO: Get a better way of finding a type (check typedefs, structs,
        # and built-in types in that order)
        type_cls = None  # typesystem.get_type()

        # Create template node
        return template.TVar(field_decl.name, self.root, parent, type_cls)

    def process_struct(self, struct_decl, parent=None, struct=None):
        """Process struct."""

        logging.debug("Processing struct [name: \"{}\"]".format(
                struct_decl.name))

        # Create the struct node if it wasn't given
        if not struct:
            struct = template.TStruct(self.root, parent)

        # Process each field
        for field in struct_decl.fields:
            if isinstance(field, ast.AstStructValueField):
                struct.add_field(self.process_var(field, struct))
            elif isinstance(field, ast.AstStructArrayField):
                struct.add_field(self.process_struct(field, struct))
            else:
                raise TemplateGeneratorException(
                    "Bad field type: \"{}\"".format(type(field)))

        return struct

    def process_root(self):
        """Process the root struct declaration."""

        logging.debug("Processing root.")

        # Locate the entrypoint structure
        entry_struct_decl = self._ast.find_symbol(TEMPLATE_ENTRY)
        if not entry_struct_decl:
            raise TemplateGeneratorException("Template entry point not found.")

        # Process root like a struct, since it basically is one kinda
        self._root = template.TRoot(TEMPLATE_ENTRY)
        return self.process_struct(entry_struct_decl, self.root, self.root)


def generate_template(target_file, ast_root):
    """Generates a template given its AST and a target file to pull data from.

    :param target_file: Opened file the template should be applied to.
    :param ast_root: AstRoot object of the AST to parse.
    """

    # TODO: perform argument sanity checking
    template_generator = TemplateGenerator(target_file, ast_root)
    return template_generator.root
