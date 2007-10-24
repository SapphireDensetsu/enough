import itertools
import weakref

class Namer(object):
    def __init__(self):
        self.index_gen = itertools.count()
        self._names = weakref.WeakKeyDictionary()

    def get_name(self, x):
        if 'name' in x.meta:
            return x.meta['name']
        if x not in self._names:
            self._names[x] = 'name_%d' % (self.index_gen.next(),)
        return self._names[x]
