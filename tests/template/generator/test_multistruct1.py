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

@pytest.mark.parametrize("loc,cls", [
    ("FILE", template.TRoot),
    ("header", template.TStruct),
    ("FILE.header", template.TStruct),
    ("GUN", template.TVar),
    ("FILE.GUN", template.TVar),
    ("ramen_4_me", template.TVar),
    ("FILE.ramen_4_me", template.TVar),
    ("header.blah0", template.TVar),
    ("FILE.header.blah0", template.TVar),
    ("header.blah1", template.TVar),
    ("FILE.header.blah1", template.TVar),
    ("header.blah2", template.TVar),
    ("FILE.header.blah2", template.TVar),
    ("header.blah3", template.TVar),
    ("FILE.header.blah3", template.TVar),
    ("header.another_thing", template.TVar),
    ("FILE.header.another_thing", template.TVar),
    ("header.so_many_things", template.TVar),
    ("FILE.header.so_many_things", template.TVar),
    ("header.data", template.TStruct),
    ("FILE.header.data", template.TStruct),
    ("header.data.hungry", template.TVar),
    ("FILE.header.data.hungry", template.TVar),
])
def test_fields(multistruct1, multistruct1_target, loc, cls):
    ast_root = parser.TemplateParser.parse_file(multistruct1)
    assert ast_root

    with open(multistruct1_target) as f:
        root = generator.generate_template(f, ast_root)
        assert root

    node = root.find_node(loc)
    assert node
    assert isinstance(node, cls)
    assert node.location == (loc if loc.startswith(template.TEMPLATE_ENTRY) else
            template.TEMPLATE_ENTRY + "." + loc)
