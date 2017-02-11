from lexer import tokens, lexer
import ply.yacc as yacc

class Struct():
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
    def __init__(self, t, n):
        self.t = t
        self.n = n

    def __repr__(self):
        return "%s %s" % (self.t, self.n)

    def __str__(self):
        return self.__repr__()

def p_struct(p):
    """ struct : STRUCT NAME LBRACE struct_field_list RBRACE SEMICOLON
    """
    p[0] = Struct(p[2], p[4])
    print(p[0])
    pass

def p_struct_field_list(p):
    """ struct_field_list : struct_field
                          | struct_field_list struct_field
    """
    p[0] = []
    if len(p) == 2:        # First option (struct_field)
        p[0].append(p[1])  # Add the new struct field to the list
    else:                  # Second option (struct_field_list struct_field)
        p[0] += p[1]       # Add the struct list to the overall list
        p[0].append(p[2])  # Add the new struct field to the list

def p_struct_field(p):
    """ struct_field : NAME NAME SEMICOLON
    """
    p[0] = Field(p[1], p[2])

sample = """
struct test {
    int field1;
    int field2;
    int blah;
};
"""

parser = yacc.yacc()
parser.parse(sample)
