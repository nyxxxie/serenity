import logging
from spade.template.ast import Ast, StructDecl, FieldDecl, ArrayDecl
from spade.template.parser import TemplateParser
from spade.typesystem import typemanager

ENTRY_STRUCT = "FILE"

class SpadeTemplateException(Exception): pass


class TNode(object):
    """Superclass for all nodes in a template.  Don't use this directly."""

    def __init__(self, name, parent, root, offset=0):
        self.name = name
        self.parent = parent
        self.root = root
        self.offset = offset
        self.size = 0

        # Figure out location
        if parent:
            self.location = parent.location + "." + name
        else:
            self.location = name

    def absolute_offset():
        """Returns the index in the file that this node's data starts at."""
        return offset

    def relative_offset():
        """Returns the offset relative to the parent this node starts at."""
        return offset - parent.offset

class TField(TNode):
    """Represents a field in a struct node."""

    def __init__(self, typedef, name, parent, root, offset=0):
        super().__init__(name, parent, root, offset)
        self.typedef = typedef
        self.data = None

    def __str__(self):
        return "{} [type:{}]".format(self.location, self.type)

    def refresh_data(self, file_, offset=None):

        # TODO: make this handle EOF properly

        if offset:
            self.offset = offset

        file_.seek(self.offset, 0)
        data = file_.read(self.typedef.size)

        self.data = self.typedef(data)
        self.size = self.data.size

    def string(self):
        if not self.data:
            return None

        return self.data.string()

    def bytes(self):
        if not self.data:
            return None

        return self.data.bytes()

#class TArray(TNode):
#    """Represents an array node."""
#
#    def __init__(self, field, offset, length, parent, root):
#        super().__init__(field.name, offset, parent, root)
#        self.length = length
#        self.field = field
#
#    def __str__(self):
#        return ("%s [type:%s] [size:%i]" % (self.location, self.field.type,
#                self.size))

class TStruct(TNode):
    """Represents a struct node."""

    def __init__(self, name, parent, root, offset=0):
        super().__init__(name, parent, root, offset)
        self.fields = []

    def __str__(self):
        ret = ("%s" % self.location)
        return ret

    def refresh_data(self, file_, offset=0):

        self.offset = offset
        self.size = 0

        for field in self.fields:
            field.refresh_data(file_, offset)
            offset += field.size
            self.size += field.size

    def field(self, location: str):
        """Gets an element relative to this element or root.

        Location is a `.`-separated path to an element that can either be
        relative to the calling node or the root node.

        `location` arg example paths: ::

            // Sample struct:
            struct ENTRY {
                struct header_t {
                    char sig[4];
                    int version;
                } header;

                struct data_item_t {
                    int data1;
                    int data2;
                }

                int data_amt;
                data_item_t data[data_amt];
            };


            // absolute (relative to root)
            "ENTRY.header.sig"

            // relative to header
            "header.sig"

            // relative to header (exclude base element)
            "sig"

        :param location: 
        :type  location: str
        :return: A :ref:`TNode <tnode>` object cooresponding to the node
                 pointed at by the 
        """

        # Split the path to get both the node to search for and 
        split = location.split(".", 1)
        cur_node = split[0]
        next_node = split[-1]

        # Determine if we're performing an absolute search
        node = self
        if cur_node == ENTRY_STRUCT:
            # Are we only requesting the root node?
            if cur_node == next_node:
                return self.root

            # If not, then process the location given after the root entry
            return self.root.field(next_node)

        # Perform a relative search
        for field in node.fields:
            if field.name == cur_node:
                # Have we reached the last element?
                if cur_node == next_node:
                    return field

                # If we haven't continue the search
                return field.field(next_node)

        # We found nothing :c
        return None


class TRoot(TStruct):
    """Represents the root of a template tree."""

    def __init__(self):
        super().__init__(ENTRY_STRUCT, None, self)

    def __str__(self):
        return pprint()

    def pprint(self, node=None, tab_level=0):

        if node is None:
            node = self

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

#def _process_array(_file, array_def, parent):
#    """Turns an AST array definition into an array template node."""
#    # Get field for this array
#    #field_def = array_def.field
#
#    # TODO: use the below variable to link the size to a template field (using field() function).
#    #size = array_def.size
#
#    # TODO: create an array of fields that is bound to this array (named something lile "whatever.huh.field[0]"
#    array = TArray(array_def.field, array_def.size, parent)
#    #for i in range(0, array_def.size):
#    #    field = _process_field(ast, file, field_def, array)
#    return array

def _process_field(field_def, parent):
    """Turns an AST field definition into a field template node.

    This function will fetch this field's type from the typemanager, and if the
    specified type is not defined will raise a SpadeTemplateException.
    """

    type_name = field_def.type
    logging.debug("Processing field: {} {}".format(type_name, field_def.name))

    Type =  typemanager.get_type(type_name)
    if not Type:
        raise SpadeTemplateException(("Invalid type \"{}\" for field "
                "\"{}\".").format(type_name, parent.location + "." +
                field_def.name))

    return TField(Type, field_def.name, parent, parent.root)

def _process_struct(struct_def, parent=None):
    """Processes an AST struct definition into a TStruct.

    Will recursively process all child structs, so calling this function on the
    root struct definition is all that's necessary to build a node tree for an
    ast.
    """

    # Determine if this struct is root
    if struct_def.name == ENTRY_STRUCT:
        struct = TRoot()
    else:
        struct = TStruct(struct_def.name, parent, parent.root)

    logging.debug("Processing struct: {}".format(struct.location))

    # Populate each struct field
    for field_def in struct_def.fields:
        if isinstance(field_def, StructDecl):
            node = _process_struct(field_def, struct)
        elif isinstance(field_def, FieldDecl):
            node = _process_field(field_def, struct)
        #elif isinstance(field, ArrayDecl):
        #    return NotImplemented
        else:
            raise SpadeTemplateException(("Invalid ast def encountered during "
                    "parse: {}").format(type(field)))

        struct.fields.append(node)

    return struct

def _process_root(target_file, root_def):
    """Processes the root node of a template.

    Root node is just a struct, so internally we process it like one.
    """

    logging.debug("Processing root node.")
    root = _process_struct(root_def)
    root.refresh_data(target_file, 0)
    return root

def from_ast(ast, target_file: str):
    """Transforms a target + a parsed AST file into a workable template.

    :param ast: Parsed STF file ast.
    :param target_file: File to apply STF to.
    """

    # Find entry point struct definition
    for struct_def in ast.structs:
        if struct_def.name == ENTRY_STRUCT:
            break
    else:
        logging.error("Couldn't find entry point in template ast.")
        return None

    # Process entry point struct
    with open(target_file, "rb") as f:
        # TODO: integrate this with Project file thing, dont read direct
        return _process_root(f, struct_def)

    logging.error("open() with statement dropped out for some reason.")
    return None

def from_file(stf_file: str, target_file: str):
    """Transforms a target + a .stf file into a workable template.

    :param stf_file: STF file.
    :param target_file: File to apply STF to.
    """

    ast = TemplateParser.parse_file(stf_file)
    if not ast:
        logging.error("Failed to parse ast file \"{}\".".format(stf_file))
        return None

    return from_ast(ast, target_file)
