import logging
from lexer import create_lexer, tokens, get_location
from ast import Struct, Field, Array, DynamicArray
import ply.yacc as yacc

logging.basicConfig(
    level = logging.DEBUG,
    filename = "log.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s")

class TemplateParser():
    def __init__(self):
        # yacc requires these be listed here in order for it to work
        self.tokens = tokens

        # Create yacc with logging enabled
        log = logging.getLogger()
        self.parser = yacc.yacc(
            module=self,
            #start='struct',
            write_tables=False,
            debug=True,
            debuglog=log)

        # Initialize other vars
        self.structs = []

    def __repr__(self):
        print("Structs:")
        for struct in structs:
            print(struct)

    def __str__(self):
        return self.__repr__()

    def parse_string(self, text):
        self.parser.parse(text, lexer=create_lexer())
        return None # TODO: need to generate structured template based on ast

    def parse_file(self, f):
        pass

    def p_struct(self, p):
        """ struct : STRUCT NAME LBRACE struct_field_list RBRACE SEMICOLON
        """
        struct = Struct(p[2], p[4])
        self._add_struct(struct)
        print(struct)
        #p[0] = struct

    def _add_struct(self, struct):
        self.structs.append(struct)

    def p_struct_field_list(self, p):
        """ struct_field_list : struct_field
                              | struct_field_list struct_field
        """
        p[0] = []
        if len(p) == 2:        # First option (struct_field)
            p[0].append(p[1])  # Add the new struct field to the list
        else:                  # Second option (struct_field_list struct_field)
            p[0] += p[1]       # Add the struct list to the overall list
            p[0].append(p[2])  # Add the new struct field to the list

    def p_struct_field_1(self, p):
        """ struct_field : TYPE NAME SEMICOLON
        """
        p[0] = Field(p[1], p[2])

    def p_struct_field_2(self, p):
        """ struct_field : TYPE NAME LBRACKET NUMBER RBRACKET SEMICOLON
        """
        p[0] = Array(Field(p[1], p[2]), p[4])

    def p_struct_field_3(self, p):
        """ struct_field : TYPE NAME LBRACKET NAME RBRACKET SEMICOLON
        """
        p[0] = DynamicArray(Field(p[1], p[2]), p[4])

    def p_error(self, p):
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

parser = TemplateParser()
template = parser.parse_string(sample))
print("---------- AST ----------")
print(parser)
print("------- TEMPLATE --------")
print(template)
print("-------------------------")
