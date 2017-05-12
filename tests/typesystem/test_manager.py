#from spade.typesystem.manager import TypeManager
#from spade.typesystem.types import default_types
#from .fixtures import typemanager
#
#def test_creation():
#    mngr = TypeManager()
#    assert mngr is not None
#
#def test_default_types_added(typemanager):
#    reported = typemanager.types()
#
#    expected = []
#    for t in default_types:
#        expected.extend(t.names)
#
#    intersect = set(reported).intersection(expected)
#    assert len(intersect) == len(reported)
