import pytest

from mold.parser import TemplateSyntaxError, parse
from mold.tokenizer import tokenize

from .common import rel

fixtures = dict(
    alltags=rel("fixtures", "alltags.mold.html"),
    unexpected_end=rel("fixtures", "unexpected_end.mold.html"),
    missing_end=rel("fixtures", "missing_end.mold.html")
)


def load(key):
    return fixtures[key], open(fixtures[key]).read()


def test_alltags():
    filename, contents = load("alltags")
    assert list(parse(tokenize(filename, contents)))


def test_unexpected_end():
    filename, contents = load("unexpected_end")
    with pytest.raises(TemplateSyntaxError):
        list(parse(tokenize(filename, contents)))


def test_missing_end():
    filename, contents = load("missing_end")
    with pytest.raises(TemplateSyntaxError):
        list(parse(tokenize(filename, contents)))
