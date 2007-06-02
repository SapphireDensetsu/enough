from WeakCollection import WeakCollection
from DisjointSets import DisjointSets
from Event import Event

from functools import partial


class DuplicateSubobjectNameError(Exception): pass

# TODO Decide whether 'name's are string or some other object that CANNOT be guessed arbitrarly

class ModelObject(object):
    builtin_meta = None
    def __init__(self, meta={}, subobjects=()):
        self.meta = meta
        if self.builtin_meta:
            self.meta.update(self.builtin_meta)
            
        self.subobjects_by_name = {}
        self.names_by_subobjects = {}
        for name, obj in subobjects:
            self.set_subobject(name, obj)

    # -------------------------------------------------------
    # Model-level code
    
    def request_subobject(self, name):
        # Causes lazy evaluation of the subobject if it doesnt exist

        # TODO protect against loops (where we request an object from ourselves causing the request function being called again)
        if name in self.subobjects_by_name:
            # This could happen ONLY if the requested subobject is
            # constant, or it is a 'source' - meaning, it does not
            # depend on other subobjects of self
            return self.subobjects_by_name[name]

        new_obj = self.generate_subobject(name)
        self.set_subobject(name, new_obj)
        return new_obj

    def generate_subobject(self, name):
        # TODO will this exist only in magic objects?
        raise NotImplementedError()

    def set_subobject(self, name, obj):
        # TODO send an event?
        if name in self.subobjects:
            raise DuplicateSubobjectNameError(name)
        self.subobjects_by_name[name] = obj
        self.names_by_subobjects[obj] = name

    def remove_subobject(self, name, obj):
        # TODO send an event?
        del self.subobjects_by_name[name]
        del self.names_by_subobjects[obj]
        
    def replace_subobject(self, name, new_obj):
        # TODO send an event?
        self.remove_subobject_by_name(name)
        self.set_subobject(name, new_obj)

    # -------------------------------------------------------
    # Python-level (implementation specific) code
    
    def remove_subobject_by_obj(self, obj):
        name = self.names_by_subobjects[obj]
        self.remove_subobject(name, obj)
    def remove_subobject_by_name(self, name):
        obj = self.subobjects_by_name[name]
        self.remove_subobject(name, obj)


##     def has_subobject_by_name(self, name):
##         # Returns True if self has for that name a subobject ready, and does not need to generate it
##         return name in self.subobjects_by_name:
##     def has_subobject_by_obj(self, obj):
##         # Returns True if self has for that name a subobject ready, and does not need to generate it
##         return obj in self.names_by_subobjects:
