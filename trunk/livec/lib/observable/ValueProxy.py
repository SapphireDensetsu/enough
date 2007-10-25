# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.observer import Observable

class _missing(object): pass

class ValueMissing(Exception): pass

class ValueProxy(object):
    def __init__(self, value=_missing):
        self.value = value
        self.obs_value = Observable()
    def exists(self):
        return self.value is not _missing
    def get(self):
        if self.value is _missing:
            raise ValueMissing()
        return self.value
    def set(self, new_value):
        old_value = self.value
        self.value = new_value
        if old_value is _missing:
            self.obs_value.notify.added(new_value)
        else:
            self.obs_value.notify.changed(old_value, new_value)
    # TODO: delete->clear
    def delete(self):
        old_value = self.value
        self.value = _missing
        self.obs_value.notify.deleted(old_value)
