# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.observer import Observable

class FuncCall(object):
    def __init__(self, func, value):
        self.func = func
        self.value = value
        self.obs_value = Observable()
        
        self._cache = self.func(value.get())
        value.obs_value.add_observer(self, '_value_')

    def _value_changed(self, old_value, new_value):
        old_cache = self._cache
        self._cache = self.func(new_value)
        self.obs_value.notify.changed(old_cache, self._cache)

    def _value_added(self, new_value):
        self._cache = self.func(new_value)
        self.obs_value.notify.added(self._cache)

    def _value_deleted(self, old_value):
        old_cache = self._cache
        del self._cache
        self.obs_value.notify.deleted(old_cache)

    def exists(self):
        return self.value.exists()
    def get(self):
        self.value.verify_exists()
        return self._cache
    def set(self, value):
        raise TypeError("Cannot set a FuncCall result")
    def clear(self, value):
        raise TypeError("Cannot clear a FuncCall result")
