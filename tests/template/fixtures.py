import os
import pytest
from spade import template

RELATIVE_DIR = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture()
def node_tree():
    """This fixture manually builds the following struct: ::

        struct header_t {
            int data;
        };

        struct idk_t {
            int f;
        }

        struct thing_t {
            idk_t idk;
        };

        struct FILE {
            int field1;
            int field2;
            header_t header;
            thing_t thing;
        };
    """

    root = template.TRoot()

    root.fields.append(template.TField(None, "field1", root, root))
    root.fields.append(template.TField(None, "field2", root, root))

    header = template.TStruct("header", root, root)
    header.fields.append(template.TField(None, "data", header, root))
    root.fields.append(header)

    thing = template.TStruct("thing", root, root)
    idk = template.TStruct("idk", thing, root)
    idk.fields.append(template.TField(None, "f", idk, root))
    thing.fields.append(idk)
    root.fields.append(thing)

    yield root

@pytest.fixture()
def singlestruct():
    """This returns the path to the singlestruct.stf file."""
    path = os.path.join(RELATIVE_DIR, "testdata", "singlestruct.stf")
    yield path

@pytest.fixture()
def singlestruct_target():
    """This returns the path to the singlestruct_target file."""
    path = os.path.join(RELATIVE_DIR, "testdata", "singlestruct_target")
    yield path
