import pytest
from spade.typesystem.manager import TypeManager

@pytest.fixture()
def typemanager():
    """
    This fixture creates and yields a typemanager object for use in tests.
    """
    mngr = TypeManager()
    yield mngr
