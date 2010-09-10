# encoding: utf-8

"""
Count Django DB queries even when DEBUG=False
"""

from contextlib import contextmanager
import inspect
import time
import sys

import django


__all__ = ['QueryCounter']


if django.VERSION < (1, 2):
    from django.db import connection
    connections = {"default": connection}
else:
    from django.db import connections as django_connections
    connections = dict((i.alias, i) for i in django_connections.all())


# Horrible monkey-patch to log query counts without requiring DEBUG = True
def _monkey_cursor_execute(conn):
    old_cursor = conn.cursor
    def new_cursor(*args, **kwargs):
        c = old_cursor(*args, **kwargs)

        old_execute = c.execute
        def new_execute(*args, **kwargs):
            try:
                return old_execute(*args, **kwargs)
            finally:
                    conn.query_count += 1
        c.execute = new_execute

        old_executemany = c.executemany
        def new_executemany(s, sql, param_list, *args, **kwargs):
            try:
                return old_executemany(s, sql, param_list, *args, **kwargs)
            finally:
                    conn.query_count += len(param_list)
        c.executemany = new_executemany

        return c

    conn.cursor = new_cursor

for conn in connections.values():
    conn.query_count = 0
    _monkey_cursor_execute(conn)



class QueryCounter(object):
    """

    Usage::
        counter = QueryCounter()
        … do something …
        for k, v in counter.deltas():
            print "Database %%s: %%d queries" % (k, v)
    """

    def __init__(self):
        self.query_counts = dict(
            (k, v.query_count) for k, v in connections.items()
        )

    def deltas(self):
        deltas = {}
        for k, v in connections.items():
            # Skip inactive connections:
            deltas[k] = v.query_count - self.query_counts[k]

        return deltas
