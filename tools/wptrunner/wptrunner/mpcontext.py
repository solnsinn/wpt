import multiprocessing

import six

_context = None


def get_context():
    global _context

    if six.PY2:
        return multiprocessing

    if _context is None:
        _context = multiprocessing.get_context("spawn")
    return _context
