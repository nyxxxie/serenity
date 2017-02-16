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
        ret += "};\n"
        return ret

    def __str__(self):
        return self.__repr__()

    def add_field(self, field):
        self.fields.append(field)

class FieldDecl():
    """ An entry in a struct """
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __repr__(self):
        return "%s %s;" % (self.type, self.name)

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
        return "%s %s[%s];" % (self.field.type, self.field.name, self.size)

    def __str__(self):
        return self.__repr__()

    def length():
        """ Returns the length of the array. """
        return self.size

class Ast():
    def __init__(self, decl_list):
        self.structs = []
        for decl in decl_list:
            if decl is StructDecl:
                self.structs.append(decl)

    def __repr__(self):
        ret = ""
        for decl in self.decl_list:
            ret += str(decl)
        return ret

    def __str__(self):
        return self.__repr__()
