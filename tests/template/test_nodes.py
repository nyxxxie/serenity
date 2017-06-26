import pytest
from tests.template.fixtures import node_tree
from spade.template import TRoot, TField, TStruct, ENTRY_STRUCT

#TODO: make a separate set of tests for TField, TArray, etc

def test_root_properties(node_tree):
    root = node_tree  # Lets make it 100% clear that this fixture = root
    assert root  # Make sure root isn't None
    assert root.root is root  # Root's root entry should be itself
    assert root.name == ENTRY_STRUCT  # Make sure it's name is right
    assert root.location == ENTRY_STRUCT  # Location too

@pytest.mark.parametrize("location,type_,name,offset,size", [
    # First some invalid locations
    ("", None, None, 0, 0),  # Empty string isn't valid
    (".", None, None, 0, 0),  # Dot might confuse the parser, lets check it
    (".blah", None, None, 0, 0),  # Leading dot might also confuse parser?
    ("dfsfa", None, None, 0, 0),  # Lets also throw a trash name at it for funzies
    (ENTRY_STRUCT + ".", None, None, 0, 0),  # ALMOST valid, but has a trailing .

    # Now some valid locations
    (ENTRY_STRUCT, TRoot, ENTRY_STRUCT, 0, 16),  # Make sure we can get the root node
    (ENTRY_STRUCT + ".field1", TField, "field1", 0, 4),  # Next of the root node's fields
    (ENTRY_STRUCT + ".field2", TField, "field2", 4, 4),  # Second field because why not
    (ENTRY_STRUCT + ".header", TStruct, "header", 8, 4),  # Lefts try looking at a struct
    (ENTRY_STRUCT + ".header.data", TField, "data", 8, 4),  # ..and a struct's field
    (ENTRY_STRUCT + ".thing", TStruct, "thing", 12, 4),  # building this query up...
    (ENTRY_STRUCT + ".thing.idk", TStruct, "idk", 12, 4),  # building this query up...
    (ENTRY_STRUCT + ".thing.idk.f", TField, "f", 12, 4),  # building this query up...
])
def test_field(node_tree, location, type_, name, offset, size):
    node = node_tree.field(location)
    if type_ is None:
        assert node is None
    else:
        assert node is not None
        assert isinstance(node, type_)
        assert node.location == location
        assert node.name == name
        assert node.offset == offset
        #assert node.size == size

def test_field_relative(node_tree):
    node = node_tree.field(ENTRY_STRUCT + ".header")
    assert node is not None

    data = node.field("data")
    assert data is not None
    assert data.name == "data"
    assert data.location == ENTRY_STRUCT + ".header.data"
    assert data.root is node_tree
