import pytest

from mold.parser import TemplateSyntaxError, parse
from mold.tokenizer import tokenize

from .common import load_fixture


def test_alltags():
    filename, contents = load_fixture("alltags")
    assert list(parse(tokenize(filename, contents)))


def test_unexpected_end():
    filename, contents = load_fixture("unexpected_end")
    with pytest.raises(TemplateSyntaxError):
        list(parse(tokenize(filename, contents)))


def test_missing_end():
    filename, contents = load_fixture("missing_end")
    with pytest.raises(TemplateSyntaxError):
        list(parse(tokenize(filename, contents)))
