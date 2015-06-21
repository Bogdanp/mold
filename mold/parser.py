from collections import namedtuple

from .tokenizer import TokenKind

Node = namedtuple("Node", ("kind", "token", "children"))
"""An abstract data type representing a template node.
"""


class TemplateSyntaxError(SyntaxError):
    """Raised when a syntax error was encountered during parsing.
    """


class PopBlock(Exception):
    """Raised when the parse stack for the current block needs to be
    popped (i.e. when an end tag has been reached).
    """


def syntax_error(token, message):
    """Raise a :class:`.TemplateSyntaxError`.

    :param Token token:
      The :class:`.Token` to reference in the error message. This is
      used to determine which file, line and column the error occurred
      at.
    :param str message:
      The error message.
    """
    return TemplateSyntaxError("{filename}:{line}:{column}: {message}".format(
        filename=token.filename,
        line=token.line, column=token.column,
        message=message
    ))


def parse_block(token, tokens):
    """Parse a nested block.

    :raises TemplateSyntaxError:
      When the token iterator has been fully consumed but a
      :class:`.PopBlock` hasn't been raised.
    :param Token token:
      The base :class:`.Token` that represents this block.
    :param Iterator tokens:
      A :class:`.Token` iterator. This is consumed until a
      :class:`.PopBlock` is raised.
    :returns:
      A block :class:`.Node`.
    """
    children = []
    try:
        for child in parse(tokens, pop=True):
            children.append(child)
    except PopBlock:
        return Node(token.kind, token, children)
    else:
        raise syntax_error(token, "missing {end}")


def parse(tokens, pop=False):
    """Parse a stream of :class:`Tokens<.Token>` into a stream of
    :class:`Nodes<.Node>`.

    :raises TemplateSyntaxError:
      When an unexpected :class:`.Token` was encountered.
    :param Iterator tokens:
      The stream of :class:`Tokens<.Token>` to consume.
    :param bool pop:
      Whether or not to pop on {end}.
    :returns:
      A :class:`.Node` generator.
    """
    for token in tokens:
        if token.kind in (
                TokenKind.when,
                TokenKind.unless,
                TokenKind.foreach,
                TokenKind.block,
                TokenKind.extend_block
        ):
            yield parse_block(token, tokens)

        elif token.kind in (
                TokenKind.chunk,
                TokenKind.raw,
                TokenKind.var,
                TokenKind.extend,
                TokenKind.include
        ):
            yield Node(token.kind, token, None)

        elif token.kind == TokenKind.end and pop:
            raise PopBlock

        else:
            raise syntax_error(token, "unexpected '{}'".format(token.kind))
