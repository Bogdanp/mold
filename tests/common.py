import os


def rel(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)
