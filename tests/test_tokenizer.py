from mold.tokenizer import Token, TokenKind, tokenize


def test_tokenize_empty_template():
    assert list(tokenize("<string>", "")) == []


def test_tokenize_tokenless_template():
    filename = "<string>"
    template = """\
<body>
    <h1>Hello!</h1>
</body>\
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, template, filename, 1, 0)
    ]


def test_tokenize_raw():
    filename = "<string>"
    template = "<body><h1>{@x}</h1></body>"
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "<body><h1>", filename, 1, 0),
        Token(TokenKind.raw, ("x", None), filename, 1, 10),
        Token(TokenKind.chunk, "</h1></body>", filename, 1, 14),
    ]

    filename = "<string>"
    template = """
<body>
    <h1>{@x}</h1>
</body>
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "\n<body>\n    <h1>", filename, 1, 0),
        Token(TokenKind.raw, ("x", None), filename, 3, 8),
        Token(TokenKind.chunk, "</h1>\n</body>\n", filename, 3, 12),
    ]

    filename = "<string>"
    template = """
<body>
    <h1>{@x.upper()}</h1>
</body>
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "\n<body>\n    <h1>", filename, 1, 0),
        Token(TokenKind.raw, ("x", ".upper()"), filename, 3, 8),
        Token(TokenKind.chunk, "</h1>\n</body>\n", filename, 3, 20),
    ]


def test_tokenize_var():
    filename = "<string>"
    template = "<body><h1>{+x.name}</h1></body>"
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "<body><h1>", filename, 1, 0),
        Token(TokenKind.var, ("x", ".name"), filename, 1, 10),
        Token(TokenKind.chunk, "</h1></body>", filename, 1, 19),
    ]

    filename = "<string>"
    template = """
<body>
    <h1>{+x}</h1>
</body>
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "\n<body>\n    <h1>", filename, 1, 0),
        Token(TokenKind.var, ("x", None), filename, 3, 8),
        Token(TokenKind.chunk, "</h1>\n</body>\n", filename, 3, 12),
    ]


def test_tokenize_end():
    filename = "<string>"
    template = "<body><h1>{end}"
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "<body><h1>", filename, 1, 0),
        Token(TokenKind.end, "{end}", filename, 1, 10),
    ]


def test_tokenize_when():
    filename = "<string>"
    template = """
<body>
    {?x}
      <h1>Hi {+x.name}</h1>
    {end}
</body>
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "\n<body>\n    ", filename, 1, 0),
        Token(TokenKind.when, ("x", None), filename, 3, 4),
        Token(TokenKind.chunk, "\n      <h1>Hi ", filename, 3, 8),
        Token(TokenKind.var, ("x", ".name"), filename, 4, 13),
        Token(TokenKind.chunk, "</h1>\n    ", filename, 4, 22),
        Token(TokenKind.end, "{end}", filename, 5, 4),
        Token(TokenKind.chunk, "\n</body>\n", filename, 5, 9),
    ]


def test_tokenize_unless():
    filename = "<string>"
    template = """
<body>
    {!x}
      <h1>Hi {+x.name}</h1>
    {end}
</body>
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "\n<body>\n    ", filename, 1, 0),
        Token(TokenKind.unless, ("x", None), filename, 3, 4),
        Token(TokenKind.chunk, "\n      <h1>Hi ", filename, 3, 8),
        Token(TokenKind.var, ("x", ".name"), filename, 4, 13),
        Token(TokenKind.chunk, "</h1>\n    ", filename, 4, 22),
        Token(TokenKind.end, "{end}", filename, 5, 4),
        Token(TokenKind.chunk, "\n</body>\n", filename, 5, 9),
    ]


def test_tokenize_foreach():
    filename = "<string>"
    template = """
<body>
    {*x}
      <h1>Hi {+item}</h1>
    {end}
</body>
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "\n<body>\n    ", filename, 1, 0),
        Token(TokenKind.foreach, ("x", None), filename, 3, 4),
        Token(TokenKind.chunk, "\n      <h1>Hi ", filename, 3, 8),
        Token(TokenKind.var, ("item", None), filename, 4, 13),
        Token(TokenKind.chunk, "</h1>\n    ", filename, 4, 20),
        Token(TokenKind.end, "{end}", filename, 5, 4),
        Token(TokenKind.chunk, "\n</body>\n", filename, 5, 9),
    ]


def test_tokenize_block():
    filename = "<string>"
    template = """
<body>
    {#a}
      <h1>Hi {+item}</h1>
    {end}
</body>
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "\n<body>\n    ", filename, 1, 0),
        Token(TokenKind.block, "a", filename, 3, 4),
        Token(TokenKind.chunk, "\n      <h1>Hi ", filename, 3, 8),
        Token(TokenKind.var, ("item", None), filename, 4, 13),
        Token(TokenKind.chunk, "</h1>\n    ", filename, 4, 20),
        Token(TokenKind.end, "{end}", filename, 5, 4),
        Token(TokenKind.chunk, "\n</body>\n", filename, 5, 9),
    ]


def test_tokenize_extend_block():
    filename = "<string>"
    template = """
<body>
    {^#a}
      <h1>Hi {+item}</h1>
    {end}
</body>
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "\n<body>\n    ", filename, 1, 0),
        Token(TokenKind.extend_block, "a", filename, 3, 4),
        Token(TokenKind.chunk, "\n      <h1>Hi ", filename, 3, 9),
        Token(TokenKind.var, ("item", None), filename, 4, 13),
        Token(TokenKind.chunk, "</h1>\n    ", filename, 4, 20),
        Token(TokenKind.end, "{end}", filename, 5, 4),
        Token(TokenKind.chunk, "\n</body>\n", filename, 5, 9),
    ]


def test_tokenize_extend():
    filename = "<string>"
    template = """{^test.html}
<body>
</body>
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.extend, "test.html", filename, 1, 0),
        Token(TokenKind.chunk, "\n<body>\n</body>\n", filename, 1, 12),
    ]


def test_tokenize_include():
    filename = "<string>"
    template = """
<body>
    {>test.html}
</body>
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "\n<body>\n    ", filename, 1, 0),
        Token(TokenKind.include, "test.html", filename, 3, 4),
        Token(TokenKind.chunk, "\n</body>\n", filename, 3, 16),
    ]


def test_tokenize_escaped_brackets():
    filename = "<string>"
    template = """
<body>
    {?x}<pre>function(x) {{ console.log(x); }</pre>{end}
</body>
"""
    assert list(tokenize(filename, template)) == [
        Token(TokenKind.chunk, "\n<body>\n    ", filename, 1, 0),
        Token(TokenKind.when, ("x", None), filename, 3, 4),
        Token(TokenKind.chunk, "<pre>function(x) { console.log(x); }</pre>", filename, 3, 8),
        Token(TokenKind.end, "{end}", filename, 3, 51),
        Token(TokenKind.chunk, "\n</body>\n", filename, 3, 56),
    ]
