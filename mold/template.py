from collections import namedtuple

from .context import Context


class Template(namedtuple("Template", ("filename", "name", "function", "blocks"))):
    """Abstract data type representing a compiled template.

    :param str filename:
      The template's filename.
    :param str name:
      The template function's name.
    :param callable function:
      The compiled template.
    :param Context blocks:
      The template's block context.
    """
    def render(self, **context):
        context = Context(self.filename, **context)
        return self.function(self.blocks, context)
