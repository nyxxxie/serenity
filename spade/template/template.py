import ast
from ast import Ast, StructDecl, FieldDecl, ArrayDecl

ENTRY_STRUCT = "FILE"

class TemplateException(Exception): pass
class ParsingException(Exception): pass

# When the user edits a template with the gui, they can select and existing
# struct in place of a type, and can create newstructs using a struct editor
# in the template editor system (maybe just have another editor).

class TNode():
    def __init__(self, template, name, parent):
        self.template = template
        self.name = name
        self.parent = parent
        self.size = 0
        self.offset = 0

        # Figure out location
        self.location = ""
        if parent is None:
            self.location += parent.location
        self.location += ("." + name)

class TField(TNode):
    def __init__(self, template, type, name, parent):
        super.__init__(template, name, parent)
        self.type = type

class TArray(TNode):
    def __init__(self, template, name, parent):
        super.__init__(template, name, parent)

class TStruct(TNode):
    def __init__(self, template, name, parent=None):
        super.__init__(template, name, parent)
        self.fields = []

class Template():
    """ Programatic representation of a template.  Uses AST definitions to
        generate a workable template that is ready to operate on a file.
    """

    def __init__(self, ast, file=None):
        self.ast = ast
        self.entry = None
        self.entry = self.process(ast, file)

    def __str__(self):
        return "Template not implemented :c"

    def __repr__(self):
        return self.__str__()

    def field(self, offset=None, path=None, scope=None):
        """ Gets field associated with an offset or path.
        """
        pass

    def process(self, ast, file):
        """ Transforms a parsed AST into a workable template. """

        # Find entry point struct definition
        ast_entry = None
        for struct in ast.structs:
            if struct.name == ENTRY_STRUCT:
                ast_entry = struct
                break
        if ast_entry is None:
            raise ParsingException("Couldn't find entrypoint.")

        # Process entry point struct
        return self._process_struct(ast, file, ast_entry)

    def reload(self):
        """ Updates template after file it is applied to is modified. """
        self.entry = process(self.ast, self.file)

    def _process_struct(self, ast, file, struct_def, parent=None):
        """ Turns an AST struct definition into a struct template node """
        struct = TStruct(self, struct_def.name, parent)

        # Process each struct field
        for decl in struct_def.field_list:
            field = None
            if type(decl) is FieldDecl:
                field = self._process_field(ast, file, decl, struct)
            elif type(decl) is ArrayDecl:
                field = self._process_array(ast, file, decl, struct)
            else:
                raise ParsingException("Encountered unhandled field type \"%s\" while parsing struct \"%s\"."
                    % (type(decl), struct.location))

        return struct

    def _process_field(self, ast, file, field_def, parent):
        """ Turns an AST field definition into a field template node """
        #field = TField(self, decl.type, decl.name, parent)
        pass

    def _process_array(self, ast, file, array_def, parent:
        """ Turns an AST array definition into an array template node """
        #field = TArray(self, decl.type, decl.name, parent)
        pass
