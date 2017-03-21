import pytest
from spade.typesystem.manager import TypeManager
from spade.typesystem.types.int32 import Int32

@pytest.fixture()
def typemanager():
    """
    This fixture creates and yields a typemanager object for use in tests.
    """
    mngr = TypeManager()
    yield mngr

@pytest.fixture()
def int32():
    """
    """
    yield Int32()
