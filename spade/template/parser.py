import logging
import ply.yacc as yacc
from spade.template import ast
from spade.template import lexer

# Disabling unused-argument because it's triggering for lexer methods that
# require a parameter be present, even if it isn't used.
# Also disabling the no-self-use check because it triggers for some reason
# on yacc methods.  Unsure as to why this is, but I think it's due to yacc
# being weird and it doesn't appear to affect anything relating to the
# execution of this program.
# pylint: disable=invalid-name,no-self-use

class TemplateParserException(Exception):
    """Raised when an issue is encountered parsing a template file."""

    pass


class TemplateParser(object):
    """Parses template files."""

    def __init__(self):
        # yacc requires these be listed here in order for it to work
        self.tokens = lexer.tokens

        # Create yacc with logging enabled
        self.parser = yacc.yacc(
            module=self,
            start='root',
            write_tables=False,
            debug=True,
            debuglog=logging.getLogger())

    def p_root(self, p):
        """ root : declaration_list
        """
        pass

    def p_declaration_list(self, p):
        """ declaration_list : declaration
                             | declaration declaration_list
        """
        pass

    def p_declaration(self, p):
        """ declaration : declaration_const
                        | declaration_array
                        | declaration_struct
        """
        pass

    def p_declaration_const(self, p):
        """ declaration_const : CONST TYPE NAME EQUALS static_value
        """
        pass

    def p_static_value(self, p):
        """ static_value : NUMBER
                         | STRING
        """
        pass

    def p_declaration_array(self, p):
        """ declaration_array : TYPE NAME LBRACKET RBRACKET EQUALS LBRACE array_value_list RBRACE SEMICOLON
        """
        pass

    def p_array_value_list(self, p):
        """ array_value_list : static_value
                             | static_value array_value_list
        """
        pass

    def p_declaration_struct(self, p):
        """ declaration_struct : STRUCT NAME LBRACE struct_contents RBRACE SEMICOLON
        """
        pass

    def p_struct_contents(self, p):
        """ struct_contents : struct_field
                            | declaration
                            | struct_field struct_contents
                            | declaration struct_contents
        """
        p[0] = []
        if len(p) == 2:        # Only 2 fields means we're at a terminal
            p[0].append(p[1])  # Add the new declaration to the list
        else:                  # Other option means we're continuing the list
            p[0].extend(p[2])  # Add the existing list to the new list
            p[0] += p[1]       # Add the new item to the new list

    def p_struct_field_1(self, p):
        """ struct_field : TYPE NAME SEMICOLON """
        p[0] = ast.AstStructValueField(p[1], p[2])

    def p_struct_field_2(self, p):
        """ struct_field : TYPE NAME LBRACKET NUMBER RBRACKET SEMICOLON
                         | TYPE NAME LBRACKET NAME RBRACKET SEMICOLON
        """
        p[0] = ast.AstStructArrayField(p[1], p[2], p[4])



    # TODO: IMPLEMENT THE ABOVE, USE THE BELOW AS REFERENCE



    #def p_ast(self, p):
    #    """ ast : body_declarations
    #    """
    #    root = ast.AstRoot()

    #    # Process each declaration in the declaration list
    #    for decl in p[1]:
    #        if isinstance(ast.AstStructDefinition, decl):
    #            root.add_struct(decl)
    #            decl.set_parent(root)
    #        #elif isinstance(ast.AstConstDefinition, decl):
    #        #    root.add_const(decl)
    #        else:
    #            raise TemplateParserException("Encountered unexpected "
    #                    "declaration type \"{}\".".format(type(decl)))

    #    p[0] = root

    #def p_body_declarations(self, p):
    #    """ body_declarations : declaration
    #                          | body_declarations declaration
    #    """
    #    p[0] = []
    #    if len(p) == 2:        # First option (declaration)
    #        p[0].append(p[1])  # Add the new declaration to the list
    #    else:                  # Second option (declaration_list struct_field)
    #        p[0] += p[1]       # Add the declaration to the overall list
    #        p[0].append(p[2])  # Add the new declaration to the list

    #def p_declaration(self, p):
    #    """ declaration : struct
    #    """
    #    p[0] = p[1]

    #def p_struct(self, p):
    #    """ struct : STRUCT NAME LBRACE struct_field_list RBRACE SEMICOLON
    #    """
    #    struct = ast.AstStructDefinition(p[2])

    #    # Add fields to struct
    #    for field in p[4]:
    #        struct.add_field(field)

    #    p[0] = struct

    #def p_struct_field_list(self, p):
    #    """ struct_field_list : struct_field
    #                          | struct_field_list struct_field
    #    """
    #    p[0] = []
    #    if len(p) == 2:        # First option (struct_field)
    #        p[0].append(p[1])  # Add the new struct field to the list
    #    else:                  # Second option (struct_field_list struct_field)
    #        p[0] += p[1]       # Add the struct list to the overall list
    #        p[0].append(p[2])  # Add the new struct field to the list

    #def p_struct_field_1(self, p):
    #    """ struct_field : TYPE NAME SEMICOLON """
    #    p[0] = ast.AstStructValueField(p[1], p[2])

    #def p_struct_field_2(self, p):
    #    """ struct_field : TYPE NAME LBRACKET NUMBER RBRACKET SEMICOLON """
    #    p[0] = ast.AstStructArrayField(p[1], p[2], p[4])

    #def p_error(self, p):
    #    if p:
    #        line, col = lexer.get_location(p)
    #        print(("Parsing error at line:{}, col:{} - Unexpected token "
    #                "\"{}\"").format(line, col, p.type))
    #    else:
    #        print("Syntax error at EOF")

    @classmethod
    def parse_string(cls, text):
        return cls().parser.parse(text, lexer=lexer.create_lexer())

    @classmethod
    def parse_file(cls, filename):
        with open(filename, "r") as f:
            return cls.parse_string(f.read())

        return None
