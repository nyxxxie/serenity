from spade.template.ast import Ast, StructDecl, FieldDecl, ArrayDecl
from spade.template.parser import TemplateParser

ENTRY_STRUCT = "FILE"

class SpadeTemplateException(Exception): pass

def pprint_template(node, tab_level=0):
    string = ("\t" * tab_level)
    if isinstance(node, TStruct):
        string += ("struct: " + str(node) + "\n")
        for field in node.fields:
            string += pprint_template(field, tab_level+1)
    if isinstance(node, TArray):
        string += ("array: " + str(node) + "\n")
    if isinstance(node, TField):
        string += ("field: " + str(node) + "\n")
    else:
        raise Exception("Unknown type encountered in template")

    return string


class TNode(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.size = 0
        self.offset = 0

        # Figure out location
        if parent:
            self.location = parent.location + "." + name
        else:
            self.location = name


class TField(TNode):
    def __init__(self, _type, name, parent):
        super().__init__(name, parent)
        self.type = _type

    def __str__(self):
        return "{} [type:{}]".format(self.location, self.type)

    def __repr__(self):
        return self.__str__()


class TArray(TNode):
    def __init__(self, field, size, parent):
        super().__init__(field.name, parent)
        self.size = size
        self.field = field

    def __str__(self):
        return ("%s [type:%s] [size:%i]" % (self.location, self.field.type,
                self.size))

    def __repr__(self):
        return self.__str__()


class TStruct(TNode):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.fields = []

    def __str__(self):
        ret = ("%s" % self.location)
        return ret

    def __repr__(self):
        return self.__str__()


def _process_struct(ast, _file, name, struct_def, parent=None):
    """Turns an AST struct definition into a struct template node."""
    struct = TStruct(name, parent)

    # Process each struct field
    for decl in struct_def.fields:
        field = None
        if isinstance(decl, FieldDecl):
            # Check to see if the type is a struct
            for ast_struct in ast.structs:
                if decl.type == struct.name:
                    print(struct)
                    field = _process_struct(ast, _file, decl.name,
                            ast_struct, struct)

            # If not a struct, it's a field (TODO: check type)
            if not field:
                field = _process_field(_file, decl, struct)
        elif isinstance(decl, ArrayDecl):
            field = _process_array(_file, decl, struct)
        else:
            raise SpadeTemplateException(("Encountered unhandled field type "
                    "\"{}\" while parsing struct \"{}\".").format(
                    str(type(decl)), struct.location))

        struct.fields.append(field)

    return struct

def _process_field(_file, field_def, parent):
    """Turns an AST field definition into a field template node."""
    # TODO: replace type with typesystem type
    _type = field_def.type
    field = TField(_type, field_def.name, parent)
    return field

def _process_array(_file, array_def, parent):
    """Turns an AST array definition into an array template node."""
    # Get field for this array
    #field_def = array_def.field

    # TODO: use the below variable to link the size to a template field (using field() function).
    #size = array_def.size

    # TODO: create an array of fields that is bound to this array (named something lile "whatever.huh.field[0]"
    array = TArray(array_def.field, array_def.size, parent)
    #for i in range(0, array_def.size):
    #    field = _process_field(ast, file, field_def, array)
    return array

def from_file(stf_file: str, target_file: str):
    """Transforms a target + a .stf file into a workable template.

    :param stf_file: STF file.
    :param target_file: File to apply STF to.
    """

    ast = TemplateParser.parse_file(stf_file)
    if not ast:
        return None

    return from_ast(ast, target_file)

def from_ast(ast, target_file: str):
    """Transforms a target + a parsed AST file into a workable template.

    :param ast: Parsed STF file ast.
    :param target_file: File to apply STF to.
    """

    # Find entry point struct definition
    ast_entry = None
    for struct in ast.structs:
        if struct.name == ENTRY_STRUCT:
            ast_entry = struct
            break

    if ast_entry is None:
        return None

    # Process entry point struct
    return _process_struct(ast, target_file, ENTRY_STRUCT, ast_entry)
