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
        p[0] = ast.AstRoot(p[1])

    def p_declaration_list(self, p):
        """ declaration_list : declaration
                             | declaration declaration_list
        """
        p[0] = [ p[1] ]
        if len(p) == 3:        # Do we have a third list element?
            p[0].extend(p[2])  # Add the next set of contents to the list

    def p_declaration(self, p):
        """ declaration : declaration_const
                        | declaration_array
                        | declaration_struct
        """
        p[0] = p[1]

    def p_declaration_const(self, p):
        """ declaration_const : CONST NAME NAME EQUALS static_value
        """
        p[0] = ast.AstConstDeclaration(p[2], p[3], p[5])

    def p_static_value(self, p):
        """ static_value : NUMBER
                         | STRING
        """
        p[0] = p[1]

    def p_declaration_array(self, p):
        """ declaration_array : NAME NAME LBRACKET RBRACKET EQUALS LBRACE array_value_list RBRACE SEMICOLON
        """
        p[0] = ast.AstArrayDeclaration(p[1], p[2], p[7])

    def p_array_value_list(self, p):
        """ array_value_list : static_value
                             | static_value array_value_list
        """
        p[0] = [ p[1] ]
        if len(p) == 3:        # Do we have a third list element?
            p[0].extend(p[2])  # Add the next set of contents to the list


    def p_declaration_struct(self, p):
        """ declaration_struct : STRUCT NAME LBRACE struct_contents RBRACE SEMICOLON
        """
        p[0] = ast.AstStructDeclaration(p[2], p[4])

    def p_struct_contents(self, p):
        """ struct_contents : struct_field
                            | declaration
                            | struct_field struct_contents
                            | declaration struct_contents
        """
        p[0] = [ p[1] ]
        if len(p) == 3:        # Do we have a third list element?
            p[0].extend(p[2])  # Add the next set of contents to the list

    def p_struct_field_1(self, p):
        """ struct_field : NAME NAME SEMICOLON """
        p[0] = ast.AstStructValueField(p[1], p[2])

    def p_struct_field_2(self, p):
        """ struct_field : NAME NAME LBRACKET NUMBER RBRACKET SEMICOLON
                         | NAME NAME LBRACKET NAME RBRACKET SEMICOLON
        """
        p[0] = ast.AstStructArrayField(p[1], p[2], p[4])

    def p_error(self, p):
        stack = ' '.join([symbol.type for symbol in self.parser.symstack][1:])
        print('Syntax error on line {}:'.format(p.lineno))
        print('\tparser state {} {} . {}'.format(self.parser.state, stack, p))

    @classmethod
    def parse_string(cls, text):
        return cls().parser.parse(text, lexer=lexer.create_lexer())

    @classmethod
    def parse_file(cls, filename):
        with open(filename, "r") as f:
            return cls.parse_string(f.read())

        return None
