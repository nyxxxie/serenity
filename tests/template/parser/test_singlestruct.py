import pytest
from tests.template.fixtures import singlestruct

from spade.template import parser
from spade.template import ast


# TODO: replace the below test function bodies with assertion helpers:
# https://docs.pytest.org/en/latest/example/simple.html#writing-well-integrated-assertion-helpers

@pytest.mark.parametrize("loc,field_amt,struct_amt,const_amt", [
    ("FILE", 3, 0, 0),
])
def test_body_structs(singlestruct, loc, field_amt, struct_amt, const_amt):
    root = parser.TemplateParser.parse_file(singlestruct)
    assert root
    assert not root.parent
    symb = root.find_symbol(loc)
    assert symb
    assert symb.parent is root
    assert symb.name == loc
    assert len(symb.fields) == field_amt
    assert len(symb.struct_decls) == struct_amt
    assert len(symb.const_decls) == const_amt

@pytest.mark.parametrize("loc,field_type,field_name,expected_cls", [
    ("FILE", "char", "magic", ast.AstStructValueField),
    ("FILE", "int", "version", ast.AstStructValueField),
    ("FILE", "int", "size", ast.AstStructValueField),
])
def test_struct_data_t(singlestruct, loc, field_type, field_name, expected_cls):
    root = parser.TemplateParser.parse_file(singlestruct)
    assert root
    assert not root.parent
    symb = root.find_symbol(loc)
    assert symb
    field = symb.find_symbol(field_name)
    assert field
    assert isinstance(field, ast.AstStructField)
    assert isinstance(field, expected_cls)
    assert field.name == field_name
    assert field.typename == field_type
