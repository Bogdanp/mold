class VariableNotFoundError(Exception):
    """Raised when a variable could not be found in the context of a
    template.
    """


class Context(dict):
    def __init__(self, filename, **context):
        super(Context, self).__init__(**context)

        self.filename = filename

    def update(self, **context):
        super(Context, self).update(**context)
        return self

    def lookup(self, key, default=None):
        """Look up a variable in the current context.

        :raises VariableNotFoundError:
          When a variable could not be found.
        :param str key:
          The variable to look up.
        :param default:
          The default value to return if the variable doesn't exist.
        :returns:
          The value of the variable.
        """
        if key not in self:
            if default is not None:
                return default

            raise VariableNotFoundError("variable '{}' not found in '{}'".format(
                key, self.filename
            ))

        return self[key]
