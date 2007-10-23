import itertools
import weakref
from gui.Stack import Stack

class BrowserWidget(Stack):
    def __init__(self):
        Stack.__init__(self)
        self.index_gen = itertools.count()
        self._names = weakref.WeakKeyDictionary()
    def get_name(self, x):
        if x not in self._names:
            self._names[x] = 'name_%d' % (self.index_gen.next(),)
        return self._names[x]
