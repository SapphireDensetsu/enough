## /* Copyright 2007, Eyal Lotem, Noam Lewis, enoughmail@googlegroups.com */
## /*
##     This file is part of Enough.

##     Enough is free software; you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation; either version 3 of the License, or
##     (at your option) any later version.

##     Enough is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>.
## */

def cached(func):
    results = {}
    def new_func(*args, **kw):
        if kw:
            return func(*args, **kw)
        
        if args not in results:
            results[args] = func(*args, **kw)
        return results[args]
    return new_func

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
        
