"""
Heap profiling using Guppy
"""

from guppy import hpy


class Heap(object):
    """
    Calculate heap consumed before and after request
    """

    def __init__(self):
        self.hp = hpy()
        self.hp.setrelheap()

    def deltas(self):
        heap = self.hp.heap()
        # TODO: Decide what other data we should include in heap reports
        return {"size": heap.size}
