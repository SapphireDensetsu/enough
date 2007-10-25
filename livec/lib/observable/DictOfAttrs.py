# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

class Error(Exception): pass

class DictOfAttrs(object):
    def __init__(self, x):
        self.x = x
        self.obs_dict = x.obs_dict

    def iteritems(self):
        for key, value in self._iteritems_from_slots():
            yield key, value
        for key, value in self._iteritems_from_dict():
            yield key, value

    def _iteritems_from_dict(self):
        x = self.x
        try:
            d = x.__dict__
        except AttributeError:
            return []
        return d.iteritems()

    def _iteritems_from_slots(self):
        x = self.x
        try:
            d = x.__slots__
        except AttributeError:
            return
        for key in d:
            yield key, getattr(self.x, key)
        
    def items(self):
        return list(self.iteritems())

    def iterkeys(self):
        for key, value in self.iteritems():
            yield key

    __iter__ = iterkeys

    def keys(self):
        return list(self.iterkeys())

    def __getitem__(self, name):
        return getattr(self.x, name)
    def __setitem__(self, name, value):
        setattr(self.x, name, value)
    def __delitem__(self, name):
        delattr(self.x, name)
