import ply.lex as lex

# Token names
tokens = (
   'NUMBER',
   'STRING',
   'LABEL',
   'LBRACE',
   'RBRACE',
   'LPAREN',
   'RPAREN',
)

# When we find a number, convert it from a string to a number
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Some regex rules for simple tokens
t_STRING = r'"(?:[^"\\]|\\.)*"'
t_LABEL  = r'[a-zA-Z][a-zA-Z0-9_\.-]*'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# This is so we cn keep track of line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def create_lexer():
    return lex.lex()
