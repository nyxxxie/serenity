import pytest
from tests.template.fixtures import multistruct1

from spade.template import parser
from spade.template import ast


@pytest.mark.parametrize("loc,field_amt,struct_amt,const_amt", [
    ("data_t", 1, 0, 0),
    ("header_t", 7, 0, 0),
    ("FILE", 3, 0, 0),
])
def test_body_structs(multistruct1, loc, field_amt, struct_amt, const_amt):
    root = parser.TemplateParser.parse_file(multistruct1)
    assert root
    symb = root.find_symbol(loc)
    assert symb
    assert symb.parent is root
    assert symb.name == loc
    assert len(symb.fields) == field_amt
    assert len(symb.struct_decls) == struct_amt
    assert len(symb.const_decls) == const_amt

@pytest.mark.parametrize("loc,field_type,field_name,expected_cls", [
    ("data_t", "int", "hungry", ast.AstStructValueField),
    ("header_t", "char", "blah0", ast.AstStructValueField),
    ("header_t", "char", "blah1", ast.AstStructValueField),
    ("header_t", "char", "blah2", ast.AstStructValueField),
    ("header_t", "char", "blah3", ast.AstStructValueField),
    ("header_t", "int", "another_thing", ast.AstStructValueField),
    ("header_t", "uint32", "so_many_things", ast.AstStructValueField),
    ("header_t", "data_t", "data", ast.AstStructValueField),
    ("FILE", "header_t", "header", ast.AstStructValueField),
    ("FILE", "int", "GUN", ast.AstStructValueField),
    ("FILE", "int", "ramen_4_me", ast.AstStructValueField),
])
def test_struct_data_t(multistruct1, loc, field_type, field_name, expected_cls):
    root = parser.TemplateParser.parse_file(multistruct1)
    assert root
    symb = root.find_symbol(loc)
    assert symb
    field = symb.find_symbol(field_name)
    assert field
    assert isinstance(field, ast.AstStructField)
    assert isinstance(field, expected_cls)
    assert field.name == field_name
    assert field.typename == field_type
