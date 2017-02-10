import ply.lex as lex

# Token names
tokens = [
   'NUMBER',
   'CHAR',
   'LABEL',
   'STRING',
   'COMMENT',
   'BCOMMENT',
   'LBRACE',
   'RBRACE',
   'LPAREN',
   'RPAREN',
   'LBRACKET',
   'RBRACKET',
   'SEMICOLON',
]

# Define specific label keywords
keywords = {
    'struct':  'STRUCT',
    'include': 'INCLUDE',
    'typedef': 'TYPEDEF',
    'if':      'IF',
    'else':    'ELSE',
}
tokens += keywords.values()

# When we find a number, convert it from a string to a number
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# When we find a number, convert it from a string to a number
def t_CHAR(t):
    r'\'([^\\\n]|(\\.))*?\''
    t.value = int(t.value)
    return t

def t_LABEL(t):
    r'[a-zA-Z][a-zA-Z0-9_\.-]*'
    if t.value in keywords:
        t.type = keywords[t.value]
    return t

def t_COMMENT(t):
    r'//.*'
    pass

def t_BCOMMENT(t):
    r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    pass

# Some regex rules for simple tokens
t_STRING    = r'\"([^\\\n]|(\\.))*?\"'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_SEMICOLON = r'\;'

# This is so we cn keep track of line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def get_coords(t):
    last_cr = t.lexer.lexdata.rfind("\n", 0, t.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (t.lexpos - last_cr)
    return (t.lexer.lineno, column)

# Error handling rule
def t_error(t):
    line, col = get_coords(t)
    print("Illegal character '%s' at [line:%i, col:%i]" % (t.value[0], line, col))
    t.lexer.skip(1) # TODO: break parsing here
