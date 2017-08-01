import sys
import pytest
import logging
from tests.template.fixtures import staticarrayfield, staticarrayfield_target

from spade.template import parser
from spade.template import template
from spade.template import generator

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_array(staticarrayfield, staticarrayfield_target):
    ast_root = parser.TemplateParser.parse_file(staticarray)
    assert ast_root

    with open(staticarray_target, "rb") as f:
        root = generator.generate_template(f, ast_root)
        assert root

    array = root.find_node("array")
    assert array
    assert isinstance(node, template.TArray)
    assert node.location == "FILE.array"
    assert node.size == 6
    assert node.length == 6
    assert node.index == 0
    assert node.offset == 0
    assert node.type_name == "char"
    assert node[0] == ord("a")
    assert node[1] == ord("b")
    assert node[2] == ord("c")
    assert node[3] == ord("d")
    assert node[4] == ord("e")
    assert node[5] == ord("f")
