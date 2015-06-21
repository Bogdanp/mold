import re

from collections import namedtuple
from functools import partial

BASE_VARIABLE_RE = r"([a-zA-Z_][a-zA-Z0-9]*)"
VARIABLE_RE = r"{}([^}}]+)?".format(BASE_VARIABLE_RE)
FILENAME_RE = r"([^}]+)"
TOKENS = (
    ("newline", r"\n"),
    ("chunk", r"[^{]+"),
    ("end", r"{end}"),
    ("escaped_bracket", r"{{"),
    ("raw", r"{{\@{var}}}".format(var=VARIABLE_RE)),
    ("var", r"{{\+{var}}}".format(var=VARIABLE_RE)),
    ("when", r"{{\?{var}}}".format(var=VARIABLE_RE)),
    ("unless", r"{{\!{var}}}".format(var=VARIABLE_RE)),
    ("foreach", r"{{\*{var}}}".format(var=VARIABLE_RE)),
    ("block", r"{{#{var}}}".format(var=BASE_VARIABLE_RE)),
    ("extend_block", r"{{\^#{var}}}".format(var=BASE_VARIABLE_RE)),
    ("extend", r"{{\^{filename}}}".format(filename=FILENAME_RE)),
    ("include", r"{{>{filename}}}".format(filename=FILENAME_RE)),
)
TOKENIZER = "|".join("(?P<{}>{})".format(k, e) for k, e in TOKENS)
TOKENIZER = re.compile(TOKENIZER)

Token = namedtuple("Token", ("kind", "value", "filename", "line", "column"))
TokenKind = type("TokenKind", (object,), {})
for kind, _ in TOKENS:
    setattr(TokenKind, kind, kind)


def tokenize(filename, template):
    """Tokenize a template.

    :raises IOError:
      When the file couldn't be read.
    :param str template:
      The contents of a template.
    :returns:
      A :class:`.Token` generator.
    """
    chunks = []  # Keep track of and merge consecutive chunks.
    chunk_like = TokenKind.newline, TokenKind.chunk, TokenKind.escaped_bracket
    line, column = 1, 0
    for match in TOKENIZER.finditer(template):
        kind = match.lastgroup
        value = match.group(kind)
        token = partial(Token, filename=filename, line=line, column=column)

        if kind in chunk_like:
            if not chunks:
                cline, ccolumn = line, column

            if kind == TokenKind.escaped_bracket:
                chunks.append(value[0])
            else:
                chunks.append(value)

            newlines = value.count("\n")
            if newlines:
                column = 0

            line += newlines
            column += len(value) - value.rfind("\n") - 1
        else:
            if chunks:
                yield Token(TokenKind.chunk, "".join(chunks), filename, cline, ccolumn)
                chunks = []

            if kind == TokenKind.end:
                yield token(kind=kind, value=value)

            elif kind in (TokenKind.include, TokenKind.extend):
                name = match.group(match.lastindex + 1)
                yield token(kind=kind, value=name)

            elif kind in (TokenKind.block, TokenKind.extend_block):
                name = match.group(match.lastindex + 1)
                yield token(kind=kind, value=name)

            else:
                variable = match.group(match.lastindex + 1)
                suffix = match.group(match.lastindex + 2)
                yield token(kind=kind, value=(variable, suffix))

            column += len(value)

    if chunks:
        yield Token(TokenKind.chunk, "".join(chunks), filename, cline, ccolumn)
