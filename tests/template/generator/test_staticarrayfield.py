import sys
import pytest
import logging
from tests.template.fixtures import staticarrayfield, staticarrayfield_target

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_array(staticarrayfield, staticarrayfield_target):
    ast_root = parser.TemplateParser.parse_file(staticarray)
    assert ast_root

    with open(staticarray_target, "rb") as f:
        root = generator.generate_template(f, ast_root)
        assert root

