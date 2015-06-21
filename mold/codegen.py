"Here be dragons."

from .context import Context
from .template import Template
from .tokenizer import TokenKind

LOOKUP = "context.lookup({!r}){}"
RAW = "str({})".format(LOOKUP)
VAR = "escape({})".format(RAW)
WHEN = "{func}(blocks, context) if {var} else ''"
UNLESS = "{func}(blocks, context) if not {var} else ''"
FOREACH = "''.join({func}(blocks, context.update(even=(i % 2 != 0), item=item)) for i, item in enumerate({var}))"
BLOCK = "blocks.lookup({var!r}, {func})(blocks, context) if blocks else {func}(blocks, context)"
EXTEND = INCLUDE = "{func}(blocks, context)"
FUNCTION = """\
def {name}(blocks, context):
  return "".join([{nodes}])\
"""


def gennested(env, var, node):
    token = node.token
    name = ":".join((token.filename, token.kind, var, str(token.line), str(token.column)))
    return env._compile(name, node.children)


def gennode(env, node, blocks):
    if node.kind not in (
            TokenKind.chunk,
            TokenKind.end,
            TokenKind.include,
            TokenKind.block,
            TokenKind.extend_block,
            TokenKind.extend,
    ):
        var, suffix = node.token.value
        var = var, suffix or ""

    if node.kind == TokenKind.chunk:
        return repr(node.token.value)

    elif node.kind == TokenKind.raw:
        return RAW.format(*var)

    elif node.kind == TokenKind.var:
        return VAR.format(*var)

    elif node.kind == TokenKind.include:
        template = env._load(node.token.value)
        return INCLUDE.format(func=template.name)

    elif node.kind == TokenKind.block:
        var = node.token.value
        template = gennested(env, var, node)
        return BLOCK.format(var=var, func=template.name)

    elif node.kind == TokenKind.extend_block:
        var = node.token.value
        template = gennested(env, var, node)
        blocks[var] = template.function
        return None

    elif node.kind == TokenKind.extend:
        template = env._load(node.token.value)
        return EXTEND.format(func=template.name)

    elif node.kind in (TokenKind.when, TokenKind.unless, TokenKind.foreach):
        template = gennested(env, "".join(var), node)
        itername = template.name
        return {
            TokenKind.when: WHEN,
            TokenKind.unless: UNLESS,
            TokenKind.foreach: FOREACH
        }[node.kind].format(func=itername, var=LOOKUP.format(*var))


def genfunc(env, filename, name, nodes):
    blocks = Context(filename)
    nodes = ", ".join(filter(lambda x: x is not None, (gennode(env, x, blocks) for x in nodes)))
    source = FUNCTION.format(name=name, nodes=nodes)
    exec(source, env.context, env.context)

    function = env.context[name]
    function.__source__ = source
    env.template_cache[name] = template = Template(filename, name, function, blocks)
    return template
