import ast

ENTRY_STRUCT = "FILE"

class TemplateException(Exception): pass

# When the user edits a template with the gui, they can select and existing
# struct in place of a type, and can create newstructs using a struct editor
# in the template editor system (maybe just have another editor).

#class Field():
#    def __init__(self, template, ast_def, parent=None):
#        pass
#
#    def name():
#        """ Returns the name of this field. """
#        pass
#
#    def offset():
#        """ Returns the offset into a file this field starts at.  """
#        pass
#
#    def size():
#        """ Returns the size of this field in bytes.  """
#        pass
#
#    def location():
#        """ Returns the location in the template tree of this field.
#            For example: "FILE.header.signature".
#        """
#        pass
#
class Struct():
    def __init__(self, template, ast_def, parent=None):
        pass

    def name():
        """ Returns the name of this struct. """
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

    def __init__(self, f, ast):
        self.ast = ast

    def __str__(self):
        return "Template not implemented :c"

    def __repr__(self):
        return self.__str__()

    def set_file(self, f):
        pass


    def get_field(offset=None, path=None):
        """ Gets field associated with an offset or path.
        """
        pass

    def get_entry():
        """ Returns the entry point struct """
        return self._entry

    def process(self):
        """ Transforms a parsed AST into a workable template. """
        # Find entry point struct
        entry_def = None
        for struct in ast.structs:
            if struct.name == ENTRY_STRUCT:
                entry_def = struct
                break

        if entry_def is None:
            return False

        # Create struct
        self.entry = self._create_struct(entry_def)
        if self.entry is None:
            return False

        return True

    def add_struct_decl(self, struct_decl):
        """ Creates a template struct from a struct definition. """
        print("About to construct struct \"%s\"." % struct_def.name)
        return None
