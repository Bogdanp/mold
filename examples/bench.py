import jinja2
import mold
import timeit

from functools import partial

m = mold.Environment(".")
j = jinja2.Environment(loader=jinja2.FileSystemLoader("."))

r1 = m.get_template("extend_example_child.mold.html").render
r2 = m.get_template("extend_example.mold.html").render
r3 = partial(m.get_template("example.mold.html").render, content="hello!", elements=["a"])

r4 = j.get_template("extend_example_child.jinja.html").render
r5 = j.get_template("extend_example.jinja.html").render
r6 = partial(j.get_template("example.jinja.html").render, content="hello", elements=["a"])

timeit = partial(timeit.timeit, number=int(1e7))

print("Sit back and relax...")
print("Mold times:")
print(timeit(r1))
print(timeit(r2))
print(timeit(r3))

print("")
print("Jinja times:")
print(timeit(r4))
print(timeit(r5))
print(timeit(r6))
