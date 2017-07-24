import sys
import pytest
import logging
from tests.template.fixtures import multistruct1, multistruct1_target

from spade.template import parser
from spade.template import template
from spade.template import generator

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# TODO: test invalid fields
# TODO: test refresh functions
# TODO: test absolute path from inner struct

@pytest.mark.parametrize("loc,type_name,cls,size,offset,data,index", [
    ("FILE", "FILE", template.TRoot, 12, 0, None, 0),
    ("header", "header_t", template.TStruct, 7, 0, None, 0),
    ("FILE.header", "header_t", template.TStruct, 7, 0, None, 0),
    ("ah", "int", template.TVar, 4, 7, bytes([0x00, 0x00, 0x00, 0x01]), 1),
    ("FILE.ah", "int", template.TVar, 4, 7, bytes([0x00, 0x00, 0x00, 0x01]), 1),
    ("ramen_4_me", "byte", template.TVar, 1, 11, bytes([0x61]), 2),
    ("FILE.ramen_4_me", "byte", template.TVar, 1, 11, bytes([0x61]), 2),
    ("header.blah0", "char", template.TVar, 1, 0, bytes([0x41]), 0),
    ("FILE.header.blah0", "char", template.TVar, 1, 0, bytes([0x41]), 0),
    ("header.blah1", "char", template.TVar, 1, 1, bytes([0x42]), 1),
    ("FILE.header.blah1", "char", template.TVar, 1, 1, bytes([0x42]), 1),
    ("header.blah2", "char", template.TVar, 1, 2, bytes([0x43]), 2),
    ("FILE.header.blah2", "char", template.TVar, 1, 2, bytes([0x43]), 2),
    ("header.blah3", "char", template.TVar, 1, 3, bytes([0x44]), 3),
    ("FILE.header.blah3", "char", template.TVar, 1, 3, bytes([0x44]), 3),
    ("header.mmmm", "byte", template.TVar, 1, 4, bytes([0x00]), 4),
    ("FILE.header.mmmm", "byte", template.TVar, 1, 4, bytes([0x00]), 4),
    ("header.asdf", "byte", template.TVar, 1, 5, bytes([0x01]), 5),
    ("FILE.header.asdf", "byte", template.TVar, 1, 5, bytes([0x01]), 5),
    ("header.data", "data_t", template.TStruct, 1, 6, None, 6),
    ("FILE.header.data", "data_t", template.TStruct, 1, 6, None, 6),
    ("header.data.q", "char", template.TVar, 1, 6, bytes([0x61]), 0),
    ("FILE.header.data.q", "char", template.TVar, 1, 6, bytes([0x61]), 0),
])
def test_fields(multistruct1, multistruct1_target, loc, type_name, cls, size,
                offset, data, index):
    ast_root = parser.TemplateParser.parse_file(multistruct1)
    assert ast_root

    with open(multistruct1_target, "rb") as f:
        root = generator.generate_template(f, ast_root)
        assert root

    node = root.find_node(loc)
    assert node
    assert isinstance(node, cls)
    assert node.location == (loc if loc.startswith(template.TEMPLATE_ENTRY) else
            template.TEMPLATE_ENTRY + "." + loc)
    assert node.size == size
    assert node.index == index
    assert node.offset == offset
    assert node.type_name == type_name
    if data:
        assert node.data.bytes() == data
