import pytest
from tests.template.fixtures import multistruct, multistruct_target
from spade import template

def test_load_template(multistruct, multistruct_target):
    root = template.from_file(multistruct, multistruct_target)
    assert root
    assert not root.parent
    assert root.name == template.ENTRY_STRUCT
    assert root.location == template.ENTRY_STRUCT
    assert root.size == 24
    assert root.offset == 0

# TODO: test field status
