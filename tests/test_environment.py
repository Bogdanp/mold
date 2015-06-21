import pytest

from mold import Environment
from mold.environment import TemplateNotFoundError

from .common import rel

env = Environment(rel("fixtures"))


def test_notfound():
    with pytest.raises(TemplateNotFoundError):
        env.get_template("idontexist.mold.html")


def test_alltags():
    template = env.get_template("alltags.mold.html")
    assert template
    assert not template.blocks


def test_cache():
    template1 = env.get_template("alltags.mold.html")
    template2 = env.get_template("alltags.mold.html")
    assert template1 == template2


def test_render():
    assert isinstance(env.render("alltags.mold.html", x="a", elements=["a", "b", "c"]), str)


def test_updating_search_paths_busts_cache():
    env.get_template("alltags.mold.html")
    assert env.filename_cache

    env.paths = env.paths
    assert not env.filename_cache


def test_render_extend():
    assert isinstance(env.render("extend.mold.html"), str)
