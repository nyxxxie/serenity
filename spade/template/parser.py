import logging
from template import Template
from lexer import create_lexer, tokens, get_location
from ast import StructDecl, FieldDecl, ArrayDecl, Ast
import ply.yacc as yacc

logging.basicConfig(
    level = logging.DEBUG,
    filename = "log.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s")

class TemplateParserException(Exception): pass

class TemplateParser():
    def __init__(self):
        # yacc requires these be listed here in order for it to work
        self.tokens = tokens

        # Create yacc with logging enabled
        log = logging.getLogger()
        self.parser = yacc.yacc(
            module=self,
            start='ast',
            write_tables=False,
            debug=True,
            debuglog=log)

        # Initialize other vars
        self.ast = Ast()

    def __repr__(self):
        return str(self.ast)

    def __str__(self):
        return self.__repr__()

    def parse_string(self, text):
        ast = self.parser.parse(text, lexer=create_lexer())
        if ast is None:
            return None

        return None # TODO: apply ast to file
        #return Template(ast)

    def parse_file(self, f):
        with open(f, "r") as f:
            return self.parse_string(f.read())

        return None

    # TODO: start work here when ast is done
    def p_ast(self, p):
        """ ast : declaration_list """
        p[0] = p[1]

    def p_declaration_list(self, p):
        """ declaration_list : declaration
                             | declaration_list declaration
        """
        p[0] = []
        if len(p) == 2:        # First option (declaration)
            p[0].append(p[1])  # Add the new declaration to the list
        else:                  # Second option (declaration_list struct_field)
            p[0] += p[1]       # Add the declaration to the overall list
            p[0].append(p[2])  # Add the new declaration to the list

    def p_declaration(self, p):
        """ declaration : struct """
        p[0] = p[1]
        pass

    def p_struct(self, p):
        """ struct : STRUCT NAME LBRACE struct_field_list RBRACE SEMICOLON
        """
        struct = StructDecl(p[2], p[4])
        self.ast.add_struct(struct)
        #p[0] = struct

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
        """ struct_field : NAME NAME SEMICOLON """
        #""" struct_field : TYPE NAME SEMICOLON """
        p[0] = FieldDecl(p[1], p[2])

    def p_struct_field_2(self, p):
        """ struct_field : NAME NAME LBRACKET NUMBER RBRACKET SEMICOLON """
        #""" struct_field : TYPE NAME LBRACKET NUMBER RBRACKET SEMICOLON """
        p[0] = ArrayDecl(FieldDecl(p[1], p[2]), p[4])

    #def p_struct_field_3(self, p):
    #    """ struct_field : NAME NAME LBRACKET NAME RBRACKET SEMICOLON """
    #    #""" struct_field : TYPE NAME LBRACKET NAME RBRACKET SEMICOLON """
    #    p[0] = ArrayDecl(FieldDecl(p[1], p[2]), p[4])

    def p_error(self, p):
        if p:
            line, col = get_location(p)
            print("Parsing error at line:%i, col:%i - Unexpected token \"%s\"" % (line, col, p.type))
        else:
            print("Syntax error at EOF")

def main():
    parser = TemplateParser()
    template = parser.parse_file("test_template.stf")
    if template == None:
        print("Failed to parse sample.")
        return

    print("---------- AST ----------")
    print(parser)
    print("------- TEMPLATE --------")
    print(template)
    print("-------------------------")

if __name__ == "__main__":
    main()
