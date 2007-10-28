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

        

def none_func(*args, **kw):
    return None

def identity(x):
    return x

class ReturnThis(object):
    # picklable alternative to lambda : x
    def __init__(self, ret_val):
        self.ret_val = ret_val
    def __call__(self):
        return self.ret_val
    
