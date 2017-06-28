import pytest
from tests.template.fixtures import singlestruct, singlestruct_target
from spade import template

def test_load_template(singlestruct, singlestruct_target):
    root = template.from_file(singlestruct, singlestruct_target)
    assert root
    assert not root.parent
    assert root.name == template.ENTRY_STRUCT
    assert root.location == template.ENTRY_STRUCT
    assert root.size == 9
    assert root.offset == 0

def test_check_field(singlestruct, singlestruct_target):
    root = template.from_file(singlestruct, singlestruct_target)
    assert root

    field = root.field("FILE.magic")
    assert field
    assert field.bytes() == bytes([0x41])
    assert field.string() == "A"

    field = root.field("FILE.version")
    assert field
    assert field.bytes() == bytes([0x00, 0x00, 0x00, 0x01])
    assert field.string() == "1"

    field = root.field("FILE.size")
    assert field
    assert field.bytes() == bytes([0x00, 0x00, 0x00, 0x00])
    assert field.string() == "0"
