# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import keyword
from functools import partial

import re
def create_convert_name_matcher():
    s = '|'.join(re.escape(kw + '_') for kw in keyword.kwlist)
    return re.compile('(%s)$' % (s,))

convert_name_matcher = create_convert_name_matcher()

def convert_name(name):
    if convert_name_matcher.search(name):
        return name[:-1]
    return name

def run_func(err, func, *args):
    if func is None:
        raise err
    return func(*args)
    
class Space(object):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.__dict__['_Space_fget']=fget
        self.__dict__['_Space_fset']=fset
        self.__dict__['_Space_fdel']=fdel
        self.__dict__['__doc__']=doc

class AttrSpace(Space):
    _get_err = AttributeError("Attributes of this object are not "
                              "readable")
    _set_err = AttributeError("Attributes of this object are not "
                              "writable")
    _del_err = AttributeError("Attributes of this object are not "
                              "deletable")
    def __getattr__(self, name):
        return run_func(self._get_err, self._Space_fget,
                        convert_name(name))

    def __setattr__(self, name, value):
        return run_func(self._set_err, self._Space_fset,
                        convert_name(name), value)
    
    def __delattr__(self, name):
        return run_func(self._del_err, self._Space_fdel,
                        convert_name(name))

class ItemSpace(Space):
    _get_err = TypeError("Items of this object are not readable")
    _set_err = TypeError("Items of this object are not writable")
    _del_err = TypeError("Items of this object are not deletable")
    def __getitem__(self, index):
        return run_func(self._get_err, self._Space_fget, index)
    
    def __setitem__(self, index, value):
        return run_func(self._set_err, self._Space_fset, index, value)
    
    def __delitem__(self, index):
        return run_func(self._del_err, self._Space_fdel, index)

def cpartial(func, *args, **kw):
    if func is None:
        return None
    return partial(func, *args, **kw)

def _space_property(space_type, fget, fset, fdel, doc):
    def get_space(self):
        fget_self = cpartial(fget, self)
        fset_self = cpartial(fset, self)
        fdel_self = cpartial(fdel, self)
        return space_type(fget_self, fset_self, fdel_self)
    return property(fget=get_space, doc=doc)

def attrspace_property(fget=None, fset=None, fdel=None, doc=None):
    return _space_property(AttrSpace, fget, fset, fdel, doc)

def itemspace_property(fget=None, fset=None, fdel=None, doc=None):
    return _space_property(ItemSpace, fget, fset, fdel, doc)
