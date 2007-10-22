from observer import Observable

class Join(Observable):
    def __init__(self, separator_factory, l):
        Observable.__init__(self)
        self.separator_factory = separator_factory
        self._cache = []
        self.l = l
        self.l.add_observer(self)
        it = iter(self.l)
        for item in it:
            self._cache.append(item)
            break
        else:
            return
        for item in it:
            self._cache.append(separator_factory())
            self._cache.append(item)
        
    def observe_insert(self, list, index, item):
        TODO
        self._cache.insert(index*2, item)
        self._cache.insert(index*2+1, self.separator_factory())
        
    def observe_pop(self, list, index):
        TODO
        self._cache.pop(index*2)
        # assumes pop was called before observe_pop
        if index == -1 or index == len(list):
            self._cache.pop(-1)
        else:
            self._cache.pop(index*2)

from proxyclass import proxy_class
Join = proxy_class(Join, '_cache', methods=[
    '__getitem__',
    '__len__',
    'index',
])
