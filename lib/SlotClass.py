# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib import observer

class MetaSlotClass(type):
    def __new__(cls, name, bases, namespace):
        if '__slots__' in namespace:
            slots = namespace['__slots__']
            if 'obs_dict' not in slots:
                slots.append('obs_dict')
        return type.__new__(cls, name, bases, namespace)

class SlotClass(object):
    __metaclass__ = MetaSlotClass
    defaults = None
    avoid_repr = ()
    def __init__(self, *args, **kw):
        self.obs_dict = observer.Observable()

        slots = list(self.__slots__)
        slots.remove('obs_dict')
        if len(args) > len(slots):
            raise TypeError("Too many arguments", args, slots)
        for field_name, arg in zip(slots, args):
            setattr(self, field_name, arg)
        defaults = self.defaults
        if defaults is None:
            defaults = {}
        for field_name in slots[len(args):]:
            try:
                value = kw.pop(field_name)
            except KeyError:
                try:
                    value = defaults[field_name]()
                except KeyError:
                    raise TypeError("Missing argument %r" % (field_name,), args, kw)
            setattr(self, field_name, value)
        if kw:
            raise TypeError("Unknown keyword arguments", kw)

    def __setattr__(self, name, value):
        if name != 'obs_dict':
            if hasattr(self, name):
                self.obs_dict.notify.replace_item(name, getattr(self, name), value)
            else:
                self.obs_dict.notify.add_item(name, value)
        
        super(SlotClass, self).__setattr__(name, value)

    def __getstate__(self):
        return tuple(getattr(self, field_name)
                     for field_name in self.__slots__
                     if field_name != 'obs_dict')

    def __setstate__(self, state):
        for name, value in zip(self.__slots__, state):
            setattr(self, name, value)

    def __repr__(self):
        t = tuple((field_name, getattr(self, field_name))
                  for field_name in self.__slots__
                  if field_name != 'obs_dict'
                  if field_name not in self.avoid_repr)
        named_values_str = ', '.join('%s=%r'%i for i in t)
        return '%s(%s)' % (self.__class__.__name__, named_values_str)
