from spade.template.parser import TemplateParser

def test_parse():
    parser = TemplateParser()
    assert parser is not None
    ast = parser.parse_file("tests/template/emptytemplate.stf")
    assert ast is None
