import pytest
from tests.template.fixtures import multistruct1, multistruct1_target

from spade.template import parser
from spade.template import generator


def test_parse(multistruct1, multistruct1_target):
    """."""

    ast_root = parser.TemplateParser.parse_file(multistruct1)
    assert ast_root

    with open(multistruct1_target) as f:
        root = generator.generate_template(f, ast_root)
        assert root
