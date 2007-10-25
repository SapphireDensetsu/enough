class SlotClass(object):
    defaults = None
    avoid_repr = ()
    def __init__(self, *args, **kw):
        if len(args) > len(self.__slots__):
            raise TypeError("Too many arguments", args, self.__slots__)
        for field_name, arg in zip(self.__slots__, args):
            setattr(self, field_name, arg)
        defaults = self.defaults
        if defaults is None:
            defaults = {}
        for field_name in self.__slots__[len(args):]:
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

    def __getstate__(self):
        return tuple(getattr(self, field_name)
                     for field_name in self.__slots__)

    def __setstate__(self, state):
        for name, value in zip(self.__slots__, state):
            setattr(self, name, value)

    def __repr__(self):
        t = tuple((field_name, getattr(self, field_name))
                  for field_name in self.__slots__
                  if field_name not in self.avoid_repr)
        named_values_str = ', '.join('%s=%r'%i for i in t)
        return '%s(%s)' % (self.__class__.__name__, named_values_str)

