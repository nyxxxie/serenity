from tests.template.fixtures import singlestruct, singlestruct_target
from spade import template

def test_load_template(singlestruct, singlestruct_target):
    template.from_file(singlestruct, singlestruct_target)
