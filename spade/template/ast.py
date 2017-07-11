"""Contains definitions for the elements of a spade template AST.

The template AST described herein is meant as a tool for translating the
elements described by a spade template file into a workable spade template.
The structures in this class should not be used directly by any casual user
seeking to work with spade templates, as they are meant to describe a more
intermediate form.
"""

class AstBody(object):
    """Base class for any AST element that requires "body" properties.

    We define "body" as a new scope for declarations.  A good rule of thumb is to
    use it whenever you use curly braces in a template file.
    """

    def __init__(self, decl_list):
        self._parent = None
        self._struct_decls = []
        self._const_decls = []
        self._entry = None

        # TODO: process decl list

    def set_parent(self, parent_body):
        self._parent = parent_body

    def find_symbol(self, name):
        """Tries to locate a symbol declaration in scope."""
        # Search constants
        for const_decl in self._const_decls:
            if struct_decl.name == name:
                return struct_decl

        # Search structs
        for struct_decl in self._struct_decls:
            if struct_decl.name == name:
                return struct_decl

        # If there's a parent, try them
        if self._parent:
            return self._parent.find_symbol(name)

        # No symbol found
        return None


class AstRoot(AstBody):
    """Root of the AST tree."""

    def __init__(self, decl_list):
        super().__init__(decl_list)


class AstDeclaration(object):
    """Base class for any AST declarations."""

    def __init__(self, type_, name):
        self._type = type_
        self._name = name


class AstConstDeclaration(AstDeclaration):
    """Declaration of a constant value."""

    def __init__(self, type_, name):
        super().__init__(type_, name)


class AstArrayDeclaration(AstConstDeclaration):
    """Declaration of a constant array."""

    def __init__(self, type_, name, size):
        super().__init__(type_, name)


class AstStructDefinition(AstBody):
    """Defines a structured contiguous sequence of data in a file."""

    def __init__(self, decl_list, field_list):
        super().__init__(decl_list)
        self._name = name
        self._fields = []

        # TODO: process field list


class AstStructField(AstDeclaration):
    """Defines a field in a structure.

    Fields different from plain declarations in that they are ordered in the
    body of a struct.
    """

    def __init__(self, type_, name):
        super().__init__(type_, name)


class AstStructValueField(AstStructField):
    """Defines a struct field that contains a single value entry.

    Note that a value field's type can either be a static type as defined in
    spade's typesystem or may be a struct defined in scope of the field.
    """

    def __init__(self, type_, name):
        super().__init__(type_, name)


class AstStructArrayField(AstStructValueField):
    """Defines a struct field that contains repeated value entries.

    Note that the given size can either be a constant value or the relative or
    absolute location of a field in scope that has an integer-like type that
    should determine the size at runtime.
    """

    def __init__(self, type_, name, size):
        super().__init__(type_, name)
        self._size = size
