from Lib.observer import Observable
import bisect

class SortedItems(object):
    def __init__(self, d):
        self.obs_list = Observable()
        d.obs_dict.add_observer(self, '_dict_')
        self._items = sorted(d.iteritems())

    def _dict_add_item(self, key, value):
        index = bisect.bisect_left(self._items, (key, value))
        self._items.insert(index, (key, value))
        self.obs_list.notify.insert(index, (key, value))
    
    def _dict_remove_item(self, key, value):
        index = bisect.bisect_left(self._items, (key, value))
        if self._items[index] != (key, value):
            import pdb
            pdb.set_trace()
        assert self._items[index] == (key, value)
        self._items.pop(index)
        self.obs_list.notify.pop(index)

    def _dict_set_item(self, key, old_value, new_value):
        self._dict_remove_item(key, old_value)
        self._dict_add_item(key, new_value)

from Lib.proxyclass import proxy_class
SortedItems = proxy_class(SortedItems, '_items', methods=[
    '__getitem__',
    '__len__',
    '__iter__',
    'index',
])
