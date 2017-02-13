from lexer import tokens, lexer, get_location
from ast import Struct, Field, Array
import ply.yacc as yacc

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

def p_struct_field_1(p):
    """ struct_field : TYPE NAME SEMICOLON
    """
    p[0] = Field(p[1], p[2])

def p_struct_field_2(p):
    """ struct_field : TYPE NAME LBRACKET NUMBER RBRACKET SEMICOLON
    """
    p[0] = Array(Field(p[1], p[2]), p[4])

def p_struct_field_3(p):
    """ struct_field : TYPE NAME LBRACKET NAME RBRACKET SEMICOLON
    """
    p[0] = Array(Field(p[1], p[2]), p[4])

def p_error(p):
    if p:
        line, col = get_location(p)
        print("Parsing error at line:%i, col:%i - Unexpected token \"%s\"" % (line, col, p.type))
    else:
        print("Syntax error at EOF")

sample = """
struct test {
    int field1;
    int field2;
    int blah;
    int blah1[1337];
    int blah2[test.field1];
};
"""

parser = yacc.yacc()
parser.parse(sample)
