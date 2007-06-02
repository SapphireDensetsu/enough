from __future__ import division
from base import ModelObject


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


def magic_obj(pyfunc, name=None):
    # A wrapper for creating magic objects with a pythonic function for generate_subobject
    class _TempMagicObject_(MagicObject):
        def generate_subobject(self, *args, **kw):
            return pyfunc(self, *args, **kw)
    if name is None:
        name = pyfunc.__name__
    return _TempMagicObject_(meta=dict(name=name))

def create_obj_maker(maker_name):
    def temp(self, name):
        return ModelObject(meta=dict(name=name, maker=self))
    return magic_obj(temp, maker_name)
    
number_maker = create_obj_maker('number maker')
bool_maker   = create_obj_maker('bool maker')


def get_addition(self, requested_name):
    # TODO change the name to 'number maker'?
    maker = self.request_subobject('maker', self)
    if requested_name == '=':
        a = self.request_subobject('a', self)
        b = self.request_subobject('b', self)
        new_obj = maker.request_subobject(a.meta['name'] + b.meta['name'], self)
    elif requested_name == 'a':
        r = self.request_subobject('=', self)
        b = self.request_subobject('b', self)
        new_obj = maker.request_subobject(r.meta['name'] - b.meta['name'], self)
    elif requested_name == 'b':
        r = self.request_subobject('=', self)
        a = self.request_subobject('a', self)
        new_obj = maker.request_subobject(r.meta['name'] - a.meta['name'], self)

    # TODO If the other objects are supplied by someone else, would it
    # make send to set the new object as a local subobject? Remember
    # that set_subobject will be called by the method that called us,
    # in ModelObject
    return new_obj
        
add = magic_obj(get_addition, '+')
add.set_subobject('maker', number_maker)


if __name__=='__main__':
    a = number_maker.request_subobject(3, None)
    b = number_maker.request_subobject(5, None)
    add.set_subobject('a', a)
    add.set_subobject('b', b)
    print add.request_subobject('=', None)
    
