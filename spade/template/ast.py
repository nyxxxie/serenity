class Struct():
    """ Contains an ordered series of data of varied types. """
    def __init__(self, name, field_list=[]):
        self.name = name
        self.field_list = field_list

    def __repr__(self):
        ret = "struct %s {\n" % (self.name)
        for field in self.field_list:
            ret += ("\t" + str(field) + "\n")
        ret += "};"
        return ret

    def __str__(self):
        return self.__repr__()

class Field():
    """ An entry in a struct """
    def __init__(self, t, n):
        self.t = t
        self.n = n

    def __repr__(self):
        return "%s %s" % (self.t, self.n)

    def __str__(self):
        return self.__repr__()

class Array():
    """ Represents an array of fields.
    Keyword arguments:
    field -- Field to array
    size  -- Size of array.  Can be either some contant or another field that contains the size.  If the latter option is used, the type of that field must convert to a number.
    """
    def __init__(self, field, size):
        self.field = field
        self.size = size

    def __repr__(self):
        return "%s[%s]" % (self.field, self.size)

    def __str__(self):
        return self.__repr__()
