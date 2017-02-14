class AstException(Exception): pass

# TODO: Figure out how AST should be organized before continuing with parser and template.  Check parser.py for the todo on where to start when ast is done

class StructDecl():
    """ Contains an ordered series of data of varied types. """
    def __init__(self, name, field_list=[]):
        self.name = name
        self.fields = field_list

    def __repr__(self):
        ret = "struct %s {\n" % (self.name)
        for field in self.fields:
            ret += ("\t" + str(field) + "\n")
        ret += "}"
        return ret

    def __str__(self):
        return self.__repr__()

    def add_field(self, field):
        self.fields.append(field)

class FieldDecl():
    """ An entry in a struct """
    def __init__(self, t, n):
        self.t = t
        self.n = n

    def __repr__(self):
        return "%s %s" % (self.t, self.n)

    def __str__(self):
        return self.__repr__()

class ArrayDecl():
    """ Represents an array of fields.
    Keyword arguments:
    field -- Field to array
    size  -- Some number > 0 representing size of array, or the location of
             some numeric field that contains this array's size.
    """
    def __init__(self, field, size):
        self.field = field
        self.size = size

    def __repr__(self):
        return "%s[%s]" % (self.field, self.size)

    def __str__(self):
        return self.__repr__()

class Ast():
    def __init__(self):
        self.structs = []

    def __repr__(self):
        ret = ""
        for struct in self.structs:
            ret += str(struct)
        return ret

    def __str__(self):
        return self.__repr__()

    def add_struct(self, struct):
        self.structs.append(struct)
        return struct
