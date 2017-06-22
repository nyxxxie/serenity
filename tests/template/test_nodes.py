import pytest
from tests.template.fixtures import node_tree
from spade.template import TRoot, TField, TStruct, ENTRY_STRUCT

# We use the entry struct name definition to make sure changes in that file
# don't break tests.  Saving it to a var here to save screen space later...
ENTRY = ENTRY_STRUCT

def test_root_properties(node_tree):
    root = node_tree  # Lets make it 100% clear that this fixture = root
    assert root  # Make sure root isn't None
    assert root.root is root  # Root's root entry should be itself
    assert root.name == ENTRY_STRUCT  # Make sure it's name is right
    assert root.location == ENTRY_STRUCT  # Location too

@pytest.mark.parametrize("location,type_,name", [
    # First some invalid locations
    ("", None, None),  # Empty string isn't valid
    (".", None, None),  # Dot might confuse the parser, lets check it
    (".blah", None, None),  # Leading dot might also confuse parser?
    ("dfsfa", None, None),  # Lets also throw a trash name at it for funzies
    (ENTRY + ".", None, None),  # ALMOST valid, but has a trailing .

    # Now some valid locations
    (ENTRY, TRoot, ENTRY),  # Make sure we can get the root node
    (ENTRY + ".field1", TField, "field1"),  # Next of the root node's fields
    (ENTRY + ".field2", TField, "field2"),  # Second field because why not
    (ENTRY + ".header", TStruct, "header"),  # Lefts try looking at a struct
    (ENTRY + ".header.data", TField, "data"),  # ..and a struct's field
    (ENTRY + ".thing", TStruct, "thing"),  # building this query up...
    (ENTRY + ".thing.idk", TStruct, "idk"),  # building this query up...
    (ENTRY + ".thing.idk.f", TField, "f"),  # building this query up...
])
def test_field(node_tree, location, type_, name):
    node = node_tree.field(location)
    if type_ is None:
        assert node is None
    else:
        assert node is not None
        assert isinstance(node, type_)
        assert node.name == name
        assert node.location == location

def test_field_relative(node_tree):
    node = node_tree.field(ENTRY + ".header")
    assert node is not None

    data = node.field("data")
    assert data is not None
    assert data.name == "data"
    assert data.location == ENTRY + ".header.data"
    assert data.root is node_tree
