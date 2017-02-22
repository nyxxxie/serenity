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
        if parent is not None:
            self.location = parent.location + "." + name
        else:
            self.location = name

class TField(TNode):
    def __init__(self, template, type, name, parent):
        super().__init__(template, name, parent)
        self.type = type

    def __str__(self):
        return ("%s [type:%s]" % (self.location, self.type))

    def __repr__(self):
        return self.__str__()

class TArray(TNode):
    def __init__(self, template, field, size, parent):
        super().__init__(template, field.name, parent)
        self.size = size
        self.field = field

    def __str__(self):
        return ("%s [type:%s] [size:%i]" % (self.location, self.field.type, self.size))

    def __repr__(self):
        return self.__str__()

class TStruct(TNode):
    def __init__(self, template, name, parent=None):
        super().__init__(template, name, parent)
        self.fields = []

    def __str__(self):
        ret = ("%s" % self.location)
        return ret

    def __repr__(self):
        return self.__str__()

def pprint_template(node, tab_level=0):
    string = ("\t" * tab_level)
    if type(node) is Template:
        string += "template:\n"
        string += pprint_template(node.entry, tab_level+1)
    elif type(node) is TStruct:
        string += ("struct: " + str(node) + "\n")
        for field in node.fields:
            string += pprint_template(field, tab_level+1)
    elif type(node) is TArray:
        string += ("array: " + str(node) + "\n")
    elif type(node) is TField:
        string += ("field: " + str(node) + "\n")
    else:
        raise Exception("Unknown type encountered in template")

    return string

class Template():
    """ Programatic representation of a template.  Uses AST definitions to
        generate a workable template that is ready to operate on a file.
    """

    def __init__(self, ast, file=None):
        self.ast = ast
        self.file = file
        self.entry = None
        self.entry = self.process(ast, file)

    def __str__(self):
        return pprint_template(self)

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
        return self._process_struct(ast, file, ENTRY_STRUCT, ast_entry)

    def reload(self):
        """ Updates template after file it is applied to is modified. """
        self.entry = process(self.ast, self.file)

    def _process_struct(self, ast, file, name, struct_def, parent=None):
        """ Turns an AST struct definition into a struct template node """
        struct = TStruct(self, name, parent)

        # Process each struct field
        for decl in struct_def.fields:
            field = None
            if type(decl) is FieldDecl:
                # Check to see if the type is a struct
                for struct_def in ast.structs:
                    if decl.type == struct_def.name:
                        print(struct_def)
                        field = self._process_struct(ast, file, decl.name, struct_def, struct)

                # If not a struct, it's a field (TODO: check type)
                if field is None:
                    field = self._process_field(ast, file, decl, struct)
            elif type(decl) is ArrayDecl:
                field = self._process_array(ast, file, decl, struct)
            else:
                raise ParsingException("Encountered unhandled field type \"%s\" while parsing struct \"%s\"."
                    % (type(decl), struct.location))

            struct.fields.append(field)

        return struct

    def _process_field(self, ast, file, field_def, parent):
        """ Turns an AST field definition into a field template node """
        # TODO: replace type with typesystem type
        type = field_def.type
        field = TField(self, type, field_def.name, parent)
        return field

    def _process_array(self, ast, file, array_def, parent):
        """ Turns an AST array definition into an array template node """
        # Get field for this array
        #field_def = array_def.field

        # TODO: use the below variable to link the size to a template field (using field() function).
        size = array_def.size

        # TODO: create an array of fields that is bound to this array (named something lile "whatever.huh.field[0]"
        array = TArray(self, array_def.field, array_def.size, parent)
        #for i in range(0, array_def.size):
        #    field = _process_field(ast, file, field_def, array)
        return array
