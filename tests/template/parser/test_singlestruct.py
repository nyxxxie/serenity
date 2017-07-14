import pytest
from tests.template.fixtures import singlestruct

from spade.template import parser
from spade.template import ast


def test_parse_file(singlestruct):
    root = parser.TemplateParser.parse_file(singlestruct)
    assert root
    assert not root._parent

# TODO: replace the below test function bodies with assertion helpers:
# https://docs.pytest.org/en/latest/example/simple.html#writing-well-integrated-assertion-helpers

@pytest.mark.parametrize("loc,field_amt,struct_amt,const_amt", [
    ("FILE", 3, 0, 0),
])
def test_body_structs(singlestruct, loc, field_amt, struct_amt, const_amt):
    root = parser.TemplateParser.parse_file(singlestruct)
    assert root
    symb = root.find_symbol(loc)
    assert symb
    assert symb._parent is root
    assert symb._name == loc
    assert len(symb._fields) == field_amt
    assert len(symb._struct_decls) == struct_amt
    assert len(symb._const_decls) == const_amt

@pytest.mark.parametrize("loc,field_type,field_name,expected_cls", [
    ("FILE", "char", "magic", ast.AstStructValueField),
    ("FILE", "int", "version", ast.AstStructValueField),
    ("FILE", "int", "size", ast.AstStructValueField),
])
def test_struct_data_t(singlestruct, loc, field_type, field_name, expected_cls):
    root = parser.TemplateParser.parse_file(singlestruct)
    assert root
    symb = root.find_symbol(loc)
    assert symb
    field = symb.find_symbol(field_name)
    assert field
    assert isinstance(field, ast.AstStructField)
    assert isinstance(field, expected_cls)
    assert field._name == field_name
    assert field._type == field_type
