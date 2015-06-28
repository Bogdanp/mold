import pytest

from mold import Environment, VariableNotFoundError

from .common import rel

env = Environment(rel("fixtures"))


def test_nil_unless():
    template = env.get_template("nil_unless.mold.html")
    assert template.render().strip() == "<h1>Hello!</h1>"
    assert template.render(idontexist=True).strip() == ""


def test_nil_if():
    template = env.get_template("nil_if.mold.html")
    assert template.render().strip() == ""
    assert template.render(idontexist=True).strip() == "<h1>Hello!</h1>"


def test_nil_foreach():
    template = env.get_template("nil_foreach.mold.html")
    assert template.render().strip() == ""
    assert template.render(idontexist=["hello"]).strip() == "<h1>hello</h1>"


def test_nil_variable():
    template = env.get_template("nil_variable.mold.html")

    with pytest.raises(VariableNotFoundError):
        template.render().strip()

    assert template.render(idontexist="hello").strip() == "<h1>hello</h1>"
