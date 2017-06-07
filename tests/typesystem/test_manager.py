from spade.typesystem.manager import TypeManager
from spade.typesystem.types import TYPE_AMOUNT
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
    assert len(typemanager._types) == TYPE_AMOUNT
