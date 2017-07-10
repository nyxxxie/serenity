"""Contains definitions for the elements of a spade template AST.

The template AST described herein is meant as a tool for translating the
elements described by a spade template file into a workable spade template.
The structures in this class should not be used directly by any casual user
seeking to work with spade templates, as they are meant to describe a more
intermediate form.
"""

class AstBody(object):
    """Base class for any AST element that sould act as a "body".

    A "body" is a 
    """

    def __init__(self, parent_body=None):
        self.parent = parent_body
        self.struct_decls = []
        self.const_decls = []
        self.entry = None

    def find_symbol(self, name):
        """Tries to locate a symbol declaration in scope."""
        # Search constants
        for const_decl in self.const_decls:
            if struct_decl.name == name:
                return struct_decl

        # Search structs
        for struct_decl in self.struct_decls:
            if struct_decl.name == name:
                return struct_decl

        # If there's a parent, try them
        if self.parent:
            return self.parent.find_symbol(name)

        # No symbol found
        return None


class AstDeclaration(object):
    """Base class for any AST declarations."""

    def __init__(self, type_, name, parent_body):
        pass


class AstRoot(AstBody):
    """Root of the AST tree."""

    def __init__(self):
        super().__init__()


class AstConstDeclaration(AstDeclaration):
    """Declaration of a constant value."""

    def __init__(self, type_, name, parent_body):
        super().__init__(type_, name, parent)


class AstArrayDeclaration(AstConstDeclaration):
    """Declaration of a constant array."""

    def __init__(self, type_, name, size, parent_body):
        super().__init__(type_, name, parent)


class AstStructDefinition(AstBody):
    """Defines a structured contiguous sequence of data in a file."""

    def __init__(self, parent):
        super().__init__(parent)
        self.fields = []


class AstStructField(AstDeclaration):
    """Defines a field in a structure.

    Fields different from plain declarations in that they are ordered in the
    body of a struct.
    """

    def __init__(self, type_, name, parent_struct)
        super().__init__(type_, name, parent_struct)


class AstStructValueField(AstStructField):
    """Defines a struct field that contains a single value entry.

    Note that a value field's type can either be a static type as defined in
    spade's typesystem or may be a struct defined in scope of the field.
    """

    def __init__(self, type_, name, parent_struct)
        super().__init__(type_, name, parent_struct)


class AstStructArrayField(AstStructValueField):
    """Defines a struct field that contains repeated value entries.

    Note that the given size can either be a constant value or the relative or
    absolute location of a field in scope that has an integer-like type that
    should determine the size at runtime.
    """

    def __init__(self, type_, name, size, parent_struct)
        super().__init__(type_, name, size, parent_struct)
