import pytest

from mold.context import Context, VariableNotFoundError


def test_context():
    c = Context("<string>", a=1)
    assert c.lookup("a") == 1
    assert c.lookup("foo", 42) == 42

    with pytest.raises(VariableNotFoundError):
        c.lookup("bar")
