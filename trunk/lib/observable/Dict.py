# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.observer import Observable
from lib.proxyclass import proxy_class

class Dict(object):
    def __init__(self, *args, **kw):
        self._dict = dict(*args, **kw)
        self.obs_dict = Observable()
        
    def __cmp__(self, other):
        if isinstance(other, Dict):
            return cmp(self._dict, other._dict)
        return cmp(self._dict, other)

    def __setitem__(self, key, value):
        if key not in self._dict:
            adding = True
        else:
            adding = False
        self._dict[key] = value
        if adding:
            self.obs_dict.notify.add_item(key, value)
        else:
            self.obs_dict.notify.set_item(key, value)
        
    def __delitem__(self, key):
        val = self._dict[key]
        del self._dict[key]
        self.obs_dict.notify.remove_item(key, val)
    
    
Dict = proxy_class(Dict, '_dict', methods=[
    '__contains__',
    '__getitem__',
    '__iter__',
    '__len__',
    'get',
    'has_key',
    'items',
    'iteritems',
    'iterkeys',
    'itervalues',
    'keys',
    'values'
])
