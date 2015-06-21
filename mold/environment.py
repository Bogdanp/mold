import hashlib
import os

from xml.sax.saxutils import escape

from .codegen import genfunc
from .context import Context
from .parser import parse
from .tokenizer import tokenize


class TemplateNotFoundError(Exception):
    """Raised when a template could not be found under any of the
    provided search paths.
    """


def normalize_name(filename):
    """Map a template file name to a template function name.

    :param str filename:
      The file name to map.
    :returns:
      The mapped function name.
    """
    return "_template_" + hashlib.md5(filename.encode("utf-8")).hexdigest()


class Environment(object):
    r"""A template environment.

    This is the primary mechanism through which templates are loaded
    from disk.

    :param list paths:
      A list of search paths. These are searched in order and the
      first match is always compiled and returned.
    :param \**context:
      Any names you would like to make avaialble in the global context
      of every compiled template.
    """

    def __init__(self, paths, **context):
        if isinstance(paths, str):
            paths = (paths,)

        self.paths_ = tuple(paths)
        self.context = dict(Context=Context, escape=escape, **context)
        self.template_cache = {}
        self.filename_cache = {}

    @property
    def paths(self):
        """Accessor for the search paths.

        :returns:
          A tuple of search paths.
        """
        return self.paths_

    @paths.setter
    def paths(self, value):
        """Setter for the search paths.

        Ensures that the underlying value is a tuple and busts the
        filename cache on every set action.

        :param tuple value:
          A tuple of search paths.
        """
        self.filename_cache = {}
        self.paths_ = tuple(value)

    def _load(self, filename):
        if filename not in self.filename_cache:
            for path in self.paths:
                filepath = os.path.join(path, filename)
                if os.path.isfile(filepath):
                    self.filename_cache[filename] = (filepath, normalize_name(filepath))
                    break
            else:
                raise TemplateNotFoundError("template '{}' not found".format(filename))

        filename, name = self.filename_cache[filename]
        if name in self.template_cache:
            return self.template_cache[name]

        with open(filename) as f:
            contents = f.read()

        return self._compile(filename, parse(tokenize(filename, contents)))

    def _compile(self, filename, nodes):
        name = normalize_name(filename)
        return genfunc(self, filename, name, nodes)

    def get_template(self, filename):
        """Load a template from disk.

        :raises TemplateNotFoundError:
          When the template could not be found.
        :param str filename:
          The name of the template to load.
        :return:
          A template.
        """
        return self._load(filename)

    def render(self, filename, **context):
        """Render a template.

        :raises VariableNotFoundError:
          If the template references a variable that wasn't provided
          in the context.
        :raises TemplateNotFoundError:
          If the template could not be found in the search path.
        :param str filename:
          The name of the template to render.
        :param \**context:
          The context with which to render the template.
        :return:
          A string representing the rendered template.
        """
        return self._load(filename).render(**context)
