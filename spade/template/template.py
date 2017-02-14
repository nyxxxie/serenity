import ast

class TemplateException(Exception): pass

# When the user edits a template with the gui, they can select and existing
# struct in place of a type, and can create newstructs using a struct editor
# in the template editor system (maybe just have another editor).

class Struct():
    __init__(self, template, ast_def, parent=None):
        pass

    def offset():
        """ Returns the offset into a file this struct starts at.
        """
        pass

    def size():
        """ Returns the size of this struct in bytes.
        """
        pass

    def location():
        """ Returns the location in the template tree of this struct.
            For example: "FILE.header.signature".
        """
        pass

class Template():
    """ Programatic representation of a template.  Uses AST definitions to
        generate a workable template that is ready to operate on a file.
    """

    def __init__(self, ast=None):
        self.ast = ast
        if self.ast is not None:
            if self._compile(ast):
                raise TemplateException("Failed to compile ast.")
        pass

    def __str__(self):
        return "Template not implemented :c"

    def __repr__(self):
        return self.__str__()

    def set_file(self, f):
        pass

    def add_ast_struct(self, struct):
        """ Useful for adding in new struct definitions """
        pass

    def get_field(offset=None, path=None):
        """ Gets field associated with an offset or path.
        """
        pass

    def _compile(self, ast):
        """ Transforms a parsed AST into a workable template. """
        # TODO: Make sure entry point exists
        return False
