import sys
import pytest
import logging
from tests.template.fixtures import staticarrayfield, staticarrayfield_target

from spade.template import parser
from spade.template import template
from spade.template import generator

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_array(staticarrayfield, staticarrayfield_target):
    ast_root = parser.TemplateParser.parse_file(staticarrayfield)
    assert ast_root

    with open(staticarrayfield_target, "rb") as f:
        root = generator.generate_template(f, ast_root)
        assert root

    array = root.find_node("array")
    assert array
    assert isinstance(node, template.TArray)
    assert array.location == "FILE.array"
    assert array.size == 6
    assert array.length == 6
    assert array.index == 0
    assert array.offset == 0
    assert array.type_name == "char"
    assert array[0] == ord("a")
    assert array[1] == ord("b")
    assert array[2] == ord("c")
    assert array[3] == ord("d")
    assert array[4] == ord("e")
    assert array[5] == ord("f")
