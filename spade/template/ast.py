class Struct():
    """ Contains an ordered series of data of varied types. """
    def __init__(self, name, field_list=[]):
        self.name = name
        self.fields = field_list

    def __repr__(self):
        ret = "struct %s {\n" % (self.name)
        for field in self.fields:
            ret += ("\t" + str(field) + "\n")
        ret += "};"
        return ret

    def __str__(self):
        return self.__repr__()

    def add_field(self, field):
        self.fields.append(field)

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
    size  -- Some number > 0 representing size of array.
    """
    def __init__(self, field, size):
        assert size > 0
        self.field = field
        self.size = size

    def __repr__(self):
        return "%s[%s]" % (self.field, self.size)

    def __str__(self):
        return self.__repr__()

class DynamicArray():
    """ Represents an array of fields.
    Keyword arguments:
    field -- Field to array
    size  -- Field in struct (either relative to this scope or global)
             representing array size.  Field's value must be representable
             as an integer.
    """
    def __init__(self, field, size):
        self.field = field
        self.size = size

    def __repr__(self):
        return "%s[%s]" % (self.field, self.size)

    def __str__(self):
        return self.__repr__()
