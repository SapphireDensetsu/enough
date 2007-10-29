# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.observer import Observable

class _Value(object):
    def __init__(self, value):
        self._value = value
        self.obs_value = Observable()
    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self._value)
    def get(self):
        return self._value

    def value_set(self, new_value):
        """Notify this _Value that the value it watches was set"""
        old_value = self._value
        self._value = new_value
        self.obs_value.notify.changed(old_value, new_value)

class ValueContainer(_Value):
    def set(self, new_value):
        self.value_set(new_value)

class ValueProxy(_Value):
    def __init__(self, setter):
        _Value.__init__(self)
        self._setter = setter

    def set(self, new_value):
        self._setter(new_value)
