import pytest
import spade.template.lexer

def test_comment():
    lexer = lex.lex(module=lexer)
    lexer.input("//this is a comment")
    i = 0
    for tok in lexer:
        i++
    assert i == 0
