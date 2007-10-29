# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.observer import Observable

class FuncCall(object):
    def __init__(self, func, *args):
        """Return an observable value that is a result of applying
        function to the given observable arguments. As long as the
        arguments are unchanging so is the get() of this value."""
        self.func = func
        self.args = args
        self.obs_value = Observable()
        
        self._update_cache()
        for arg in self.args:
            arg.obs_value.add_observer(self, '_arg_')

    def _update_cache(self):
        self._cache = self.func(*(arg.get() for arg in self.args))

    def _arg_changed(self, old_arg, new_arg):
        old_cache = self._cache
        self._update_cache()
        self.obs_value.notify.changed(old_cache, self._cache)

    def get(self):
        return self._cache
    def set(self, value):
        raise TypeError("Cannot set a FuncCall result")
