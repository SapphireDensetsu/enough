# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.observer import Observable

class List(object):
    def __init__(self, *args, **kw):
        self.obs_list = Observable()
        self._items = list(*args, **kw)

    def insert(self, index, item):
        self._items.insert(index, item)
        self.obs_list.notify.insert(index, item)
    
    def pop(self, index=-1):
        value = self._items.pop(index)
        self.obs_list.notify.pop(index, value)

    def remove(self, item):
        self.pop(self.index(item))

    def append(self, item):
        self.insert(len(self), item)

from lib.proxyclass import proxy_class
List = proxy_class(List, '_items', methods=[
    '__getitem__',
    '__len__',
    '__iter__',
    'index',
])
