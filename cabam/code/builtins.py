from __future__ import division
import base


class MagicObject(ModelObject):
    builtin_meta = dict(magic=True)
    
class ObjectMaker(MagicObject):
    def generate_subobject(self, name):
        return ModelObject(meta=dict(maker=self))

# The root maker of all objects
root_object_maker = ObjectMaker(meta=dict(name='root object maker'))


def create_obj(name):
    # Create a new object using the root object maker
    obj = root_object_maker.request_subobject(name)
    obj.meta['name'] = metaname
    return obj


def magic_obj(name=None):
    # A wrapper for creating magic objects with a pythonic function for generate_subobject
    def dec(func):
        class _TempMagicObject_(MagicObject):
            def generate_subobject(self, *args, **kw):
                return func(self, *args, **kw)
        if name is None:
            name = func.__name__
        return _TempMagicObject_(meta=dict(name=name))
    return dec

def create_obj_maker(maker_name):
    def temp(self, name):
        return ModelObject(meta=dict(name=name, maker=self))
    return magic_obj(maker_name)(temp)
    
number_maker = create_obj_maker('number maker')
bool_maker   = create_obj_maker('bool maker')



@magic_obj('+')
def get_addition(self, requested_name):
    maker = self.request_subobject('maker')
    if requested_name == '=':
        # TODO use some in-model mechanism to report this error
        a = self.request_subobject('a')
        b = self.request_subobject('b')
        # TODO change the name to 'result maker'?
        maker.request_subobject(a.meta['name'] + b.meta['name'])
    elif requested_name == 'a':
        r = self.request_subobject('=')
        b = self.request_subobject('b')
        maker.request_subobject(r.meta['name'] - b.meta['name'])
    elif requested_name == 'b':
        r = self.request_subobject('=')
        a = self.request_subobject('a')
        maker.request_subobject(r.meta['name'] - a.meta['name'])

