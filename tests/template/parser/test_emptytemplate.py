from tests.template.parser.fixtures import emptytemplate
from spade.template.parser import TemplateParser

def test_parse(emptytemplate):
    parser = TemplateParser()
    assert parser is not None
    ast = parser.parse_file(emptytemplate)
    assert ast is None
