from spade.typesystem.manager import TypeManager
from spade.typesystem.types import type_amt
from spade.typesystem import typemanager

# ---------------------------
# TypeManager TESTS
# ---------------------------
def test_init():
    mngr = TypeManager()
    assert len(mngr._types) == 0


# ---------------------------
# typemanager TESTS
# ---------------------------
def test_typemanager_types_added():
    assert typemanager is not None
    assert len(typemanager.types()) == type_amt
