import pytest
import logging
from tests.template.fixtures import multistruct1, multistruct1_target

from spade.template import parser
from spade.template import generator

logging.basicConfig(level=logging.DEBUG)


def test_parse(multistruct1, multistruct1_target):
    """."""

    ast_root = parser.TemplateParser.parse_file(multistruct1)
    assert ast_root

    with open(multistruct1_target) as f:
        root = generator.generate_template(f, ast_root)
        assert root
