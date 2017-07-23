"""Turns an AST into a template structure.

This module implements the template system's semantic analyser and template
structure generator.  The end result is a tree-like template structure as
defined in (TODO: ref here) template.py.  It is reccomended that these methods
not be used directly by most common users, as the __init__.py file in this
directory contains convenient helper functions that shorten common template
generation operations to a single function call.
"""

import logging
from spade.typesystem import typemanager
from spade.template import ast
from spade.template import template



class GeneratorError(Exception):
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

    def refresh(self, target_file):
        if self.root:
            self.root.refresh(target_file)

    def process_field(self, field_decl, parent_ast=None, parent=None):
        """Process var."""

        logging.debug("Processing var [type: \"{}\", name: \"{}\"]".format(
                field_decl.typename, field_decl.name))


        symb = parent_ast.find_symbol(field_decl.typename)
        if symb:
            if isinstance(symb, ast.AstStructDeclaration):
                logging.debug("Determined type {} is a struct ".format(
                        field_decl.typename))
                return self.process_struct(field_decl.name, symb, parent)
            # elif: TODO: process typedefs
            else:
                raise GeneratorError("Unexpected type {} specified for struct "
                        "element {}".format(type(symb), field_decl.name))


        # If we didn't find any symbol, check the typesystem.
        symb = typemanager.get_type(field_decl.typename)
        if symb:
            logging.debug("Determined type {} is a native type.".format(
                    field_decl.typename))
            return template.TVar(field_decl.name, self.root, parent, symb)

        # If we didn't find a definition for the type, we're SOL
        raise GeneratorError("Undefined type {} specified for struct element "
                "{}".format(field_decl.typename, field_decl.name))

    def process_struct(self, field_name, struct_decl, parent=None, struct=None):
        """Process struct."""

        logging.debug("Processing struct [name: \"{}\"]".format(field_name))

        # Create the struct node if it wasn't given
        if not struct:
            struct = template.TStruct(field_name, self.root, parent)

        # Process each field
        for field in struct_decl.fields:
            if isinstance(field, ast.AstStructValueField):
                struct.add_field(self.process_field(field, struct_decl, struct))
            elif isinstance(field, ast.AstStructArrayField):
                raise NotImplemented("Arrays are not implemented.")
            else:
                raise GeneratorError("Bad field type \"{}\"".format(type(field)))

        return struct

    def process_root(self):
        """Process the root struct declaration."""

        logging.debug("Processing root.")

        # Locate the entrypoint structure
        entry_struct_decl = self._ast.find_symbol(template.TEMPLATE_ENTRY)
        if not entry_struct_decl:
            raise GeneratorError("Template entry point not found.")

        # Process root like a struct, since it basically is one kinda
        self._root = template.TRoot(template.TEMPLATE_ENTRY)
        return self.process_struct(template.TEMPLATE_ENTRY, entry_struct_decl,
                                   self.root, self.root)


def generate_template(target_file, ast_root):
    """Generates a template given its AST and a target file to pull data from.

    :param target_file: Opened file the template should be applied to.
    :param ast_root: AstRoot object of the AST to parse.
    """

    # TODO: perform argument sanity checking
    template_generator = TemplateGenerator(target_file, ast_root)
    template_generator.refresh(target_file)
    return template_generator.root
