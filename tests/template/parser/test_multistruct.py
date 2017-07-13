from tests.template.fixtures import multistruct

from spade.template import parser
from spade.template import ast


def test_parse_file(multistruct):
    root = parser.TemplateParser.parse_file(multistruct)
    assert root
    # TODO: move this and other test shit to parser directory?  Makes more sense to test the parser and AST shit there
