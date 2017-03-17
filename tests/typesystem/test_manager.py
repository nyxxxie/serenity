from spade.typesystem.manager import TypeManager
from spade.typesystem.types import default_types
from .fixtures import typemanager

def test_creation():
    mngr = TypeManager()
    assert mngr is not None

def test_default_types_added(typemanager):
    reported = typemanager.types()
    expected = [x.name for x in default_types]
    intersect = set(reported).intersection(expected)
    assert len(intersect) == len(default_types)
