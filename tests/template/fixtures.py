import os
import pytest
from spade import template
from spade.typesystem.types import int32

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

    root.fields.append(template.TField(int32.Int32, "field1", 0, root, root))
    root.fields.append(template.TField(int32.Int32, "field2", 4, root, root))

    header = template.TStruct("header", 8, root, root)
    header.fields.append(template.TField(int32.Int32, "data", 8, header, root))
    root.fields.append(header)

    thing = template.TStruct("thing", 12, root, root)
    idk = template.TStruct("idk", 12, thing, root)
    idk.fields.append(template.TField(int32.Int32, "f", 12, idk, root))
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
