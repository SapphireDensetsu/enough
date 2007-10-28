import bisect
from lib.observable.ValueContainer import ValueProxy

class _ListItem(object):
    def __init__(self, list_, index):
        self.list_ = list_
        self.index = index
        self.value = ValueProxy(self._set_value, self._del_value)
        self.value.value_set(self.list_[index])

    def __cmp__(self, other):
        return cmp(self.index, other)

    def _moved(self, delta):
        self.index += delta

    def _set_value(self, value):
        self.list_[self.index] = value

    def _del_value(self):
        del self.list_[self.index]

class ListProxy(object):
    def __init__(self, list_):
        self.list_ = list_
        self.list_.obs_list.add_observer(self, '_list_')
        self._list_items = []

    def proxy(self, index):
        l = _ListItem(self.list_, index)
        bisect.insort(self._list_items, l)
        return l.value

    def _list_insert(self, index, item):
        start_index = bisect.bisect_left(self._list_items, index)
        for l in self._list_items[start_index:]:
            l._moved(1)

    def _list_pop(self, index, value):
        start_index = bisect.bisect_left(self._list_items, index)
        if start_index >= len(self._list_items):
            return
        to_remove = []
        for rel_index, list_item in enumerate(self._list_items[start_index:]):
            if list_item.index == index:
                # TODO: This is fishy.. We can understand when a Proxy
                # to an index dies (popped) but not when one is
                # inserted. Teh value is cleared and never set
                # again. Does this make sense?
                list_item.value.value_cleared()
                list_item.index = None
                to_remove.append(rel_index+start_index)
            else:
                list_item._moved(-1)
        for index in to_remove[::-1]:
            self._list_items.pop(index)

    def _list_replace(self, index, old_value, new_value):
        start_index = bisect.bisect_left(self._list_items, index)
        if start_index >= len(self._list_items):
            return
        for l in self._list_items[start_index:]:
            if l.index != index:
                return
            l.value.value_set(new_value)
