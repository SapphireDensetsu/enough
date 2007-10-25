from lib.observable.ValueProxy import ValueProxy

class AlreadyMapped(Exception): pass

class DictMap(object):
    """Maps some of an observable input dict's keys to observable
    value proxies"""
    def __init__(self, d):
        self.d = d
        self.d.obs_dict.add_observer(self, '_dict_')
        self._mapping = {}
    def map(self, key, func):
        if key in self._mapping:
            raise AlreadyMapped(key)
        if key in self.d:
            value_proxy = ValueProxy(func(self.d[key]))
        else:
            value_proxy = ValueProxy()
        
        self._mapping[key] = func, value_proxy
        return value_proxy
    
    def _dict_add_item(self, key, value):
        if key not in self._mapping:
            return
        func, value_proxy = self._mapping[key]
        value_proxy.set(func(value))
    
    def _dict_remove_item(self, key, value):
        if key not in self._mapping:
            return
        func, value_proxy = self._mapping[key]
        value_proxy.delete()

    def _dict_replace_item(self, key, old_value, new_value):
        if key not in self._mapping:
            return
        func, value_proxy = self._mapping[key]
        value_proxy.set(func(new_value))
