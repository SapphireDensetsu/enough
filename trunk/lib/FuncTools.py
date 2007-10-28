# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from functools import partial

class PicklablePartial(object):
    def __init__(self, *args, **kw):
        self._args = args
        self._kw = kw
        self._set_partial()
        
    def __call__(self, *args, **kw):
        return self._partial(*args, **kw)
    def _set_partial(self):
        self._partial = partial(*self._args, **self._kw)
        
    def __getstate__(self):
        return self._args, self._kw
    def __setstate__(self, (a,k)):
        self._args = a
        self._kw = k
        self._set_partial()
