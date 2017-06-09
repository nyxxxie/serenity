class AstException(Exception): pass

class StructDecl(object):
    """Contains an ordered series of data of varied types."""

    def __init__(self, name, field_list=None):
        self.name = name
        self.fields = [] if not field_list else field_list

    def __repr__(self):
        ret = "struct %s {\n" % (self.name)
        for field in self.fields:
            ret += ("\t" + str(field) + "\n")
        ret += "};\n"
        return ret

    def __str__(self):
        return self.__repr__()

    def add_field(self, field):
        self.fields.append(field)

class FieldDecl(object):
    """An entry in a struct."""

    def __init__(self, _type, name):
        self.type = _type
        self.name = name

    def __repr__(self):
        return "%s %s;" % (self.type, self.name)

    def __str__(self):
        return self.__repr__()

class ArrayDecl(object):
    """Represents an array of fields."""

    def __init__(self, field, size):
        self.field = field
        self.size = size

    def __repr__(self):
        return "%s %s[%s];" % (self.field.type, self.field.name, self.size)

    def __str__(self):
        return self.__repr__()

    def length(self):
        """Returns the length of the array."""
        return self.size

class Ast(object):
    """AST ."""

    def __init__(self, decl_list):
        self.structs = []
        for decl in decl_list:
            if isinstance(decl, StructDecl):
                self.structs.append(decl)

    def __repr__(self):
        ret = ""
        for struct in self.structs:
            ret += str(struct)
        return ret

    def __str__(self):
        return self.__repr__()

    def struct(self, name):
        for struct in self.structs:
            if struct.name == name:
                return struct
        return None
