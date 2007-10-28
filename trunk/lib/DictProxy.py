# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.observable.ValueContainer import ValueProxy
from lib.observable.FuncCall import FuncCall
from lib.FuncTools import PicklablePartial as partial

class AlreadyMapped(Exception): pass

class DictProxy(object):
    """Maps some of an observable input dict's keys to observable
    value proxies"""
    def __init__(self, d):
        self.d = d
        self.d.obs_dict.add_observer(self, '_dict_')
        self._mapping = {}

    def _set_value(self, key, value):
        self.d[key] = value

    def _del_value(self, key):
        del self.d[key]

    def proxy(self, key):
        if key in self._mapping:
            raise AlreadyMapped(key)
        value_proxy = ValueProxy(partial(self._set_value, key),
                                 partial(self._del_value, key))
        self._mapping[key] = value_proxy
        if key in self.d:
            value_proxy.value_set(self.d[key])
        else:
            value_proxy.value_cleared()
        return value_proxy

    # TODO: Get rid of this method
    def map(self, key, func):
        return FuncCall(func, self.proxy(key))
    
    def _dict_add_item(self, key, value):
        if key not in self._mapping:
            return
        value_proxy = self._mapping[key]
        value_proxy.value_set(value)
    
    def _dict_remove_item(self, key, value):
        if key not in self._mapping:
            return
        value_proxy = self._mapping[key]
        value_proxy.value_cleared()

    def _dict_replace_item(self, key, old_value, new_value):
        if key not in self._mapping:
            return
        value_proxy = self._mapping[key]
        value_proxy.value_set(new_value)
