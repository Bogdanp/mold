import os


def rel(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)


fixtures = dict(
    alltags=rel("fixtures", "alltags.mold.html"),
    unexpected_end=rel("fixtures", "unexpected_end.mold.html"),
    missing_end=rel("fixtures", "missing_end.mold.html"),
    nil_unless=rel("fixtures", "nil_unless.mold.html"),
)


def load_fixture(key):
    return fixtures[key], open(fixtures[key]).read()
