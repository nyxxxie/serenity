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

# TODO: check fields
