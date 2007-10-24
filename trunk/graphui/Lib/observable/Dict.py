from Lib.observer import Observable
from Lib.proxyclass import proxy_class

class Dict(object):
    def __init__(self, *args, **kw):
        self._dict = dict(*args, **kw)
        self.obs_dict = Observable()
        
    def __cmp__(self, other):
        if isinstance(other, Dict):
            return self._dict.__comp__(other._dict)
        return self._dict.__cmp__(other)

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
        del self._dict[key]
        self.obs_dict.notify.remove_item(key)
    
    
Dict = proxy_class(Dict, '_dict', methods=[
    '__contains__',
    '__eq__',
    '__ge__',
    '__getitem__',
    '__gt__',
    '__iter__',
    '__le__',
    '__len__',
    '__lt__',
    '__ne__',
    'get',
    'has_key',
    'items',
    'iteritems',
    'iterkeys',
    'itervalues',
    'keys',
    'values'
])
