from tests.template.parser.fixtures import basictemplate
from spade.template.parser import TemplateParser

def test_parse(basictemplate):
    # Parse template
    parser = TemplateParser()
    assert parser is not None
    ast = parser.parse_file(basictemplate)
    assert ast is not None

    # Do we have all our structs?
    assert ast.structs is not None
    assert len(ast.structs) == 1
    assert "FILE" in [x.name for x in ast.structs]
