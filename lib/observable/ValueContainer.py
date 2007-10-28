# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.observer import Observable

class _missing(object): pass

class ValueMissing(Exception): pass

class _Value(object):
    def __init__(self, value=_missing):
        self.value = value
        self.obs_value = Observable()
    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.value)
    def exists(self):
        return self.value is not _missing
    def verify_exists(self):
        if self.value is _missing:
            raise ValueMissing()
    def get(self):
        self.verify_exists()
        return self.value

    def value_set(self, new_value):
        """Notify this _Value that the value it watches was set"""
        old_value = self.value
        self.value = new_value
        if old_value is _missing:
            self.obs_value.notify.added(new_value)
        else:
            self.obs_value.notify.changed(old_value, new_value)
    def value_cleared(self):
        """Notify this _Value that the value it watches was cleared"""
        old_value = self.value
        self.value = _missing
        self.obs_value.notify.deleted(old_value)

class ValueContainer(_Value):
    def set(self, new_value):
        self.value_set(new_value)
    def clear(self):
        self.value_cleared(new_value)

class ValueProxy(_Value):
    def __init__(self, setter, clearer=None):
        _Value.__init__(self)
        self._setter = setter
        self._clearer = clearer

    def set(self, new_value):
        self._setter(new_value)

    def clear(self):
        if self._clearer is None:
            raise TypeError("%r clear not supported" % (self,))
        self._clearer()
