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

@pytest.mark.parametrize("loc,cls,size,data", [
    ("FILE", template.TRoot, 24, None),
    ("header", template.TStruct, 16, None),
    ("FILE.header", template.TStruct, 16, None),
    ("GUN", template.TVar, 4, bytes([0x00, 0x00, 0x00, 0x04])),
    ("FILE.GUN", template.TVar, 4, bytes([0x00, 0x00, 0x00, 0x04])),
    ("ramen_4_me", template.TVar, 4, bytes([0x00, 0x00, 0x00, 0xFF])),
    ("FILE.ramen_4_me", template.TVar, 4, bytes([0x00, 0x00, 0x00, 0xFF])),
    ("header.blah0", template.TVar, 1, bytes([0x41])),
    ("FILE.header.blah0", template.TVar, 1, bytes([0x41])),
    ("header.blah1", template.TVar, 1, bytes([0x41])),
    ("FILE.header.blah1", template.TVar, 1, bytes([0x41])),
    ("header.blah2", template.TVar, 1, bytes([0x41])),
    ("FILE.header.blah2", template.TVar, 1, bytes([0x41])),
    ("header.blah3", template.TVar, 1, bytes([0x41])),
    ("FILE.header.blah3", template.TVar, 1, bytes([0x41])),
    ("header.mmmm", template.TVar, 4, bytes([0x00, 0x00, 0x00, 0x01])),
    ("FILE.header.mmmm", template.TVar, 4, bytes([0x00, 0x00, 0x00, 0x01])),
    ("header.asdf", template.TVar, 4, bytes([0x00, 0x00, 0x00, 0x01])),
    ("FILE.header.asdf", template.TVar, 4, bytes([0x00, 0x00, 0x00, 0x01])),
    ("header.data", template.TStruct, 4, None),
    ("FILE.header.data", template.TStruct, 4, None),
    ("header.data.q", template.TVar, 4, bytes([0x00, 0x00, 0x00, 0x01])),
    ("FILE.header.data.q", template.TVar, 4, bytes([0x00, 0x00, 0x00, 0x01])),
])
def test_fields(multistruct1, multistruct1_target, loc, cls, size, data):
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
    if data:
        assert node.data.bytes() == data