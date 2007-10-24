from Lib.Space import attrspace_property

# TODO: When do we remove_observer? Use weakref?
class Observable(object):
    def __init__(self):
        self.observers = {}
    def add_observer(self, observer, prefix, *args, **kw):
        self.observers[observer] = (prefix, args, kw)
    def remove_observer(self, observer):
        del self.observers[observer]

    def get_notifier(self, name):
        def func(*args, **kw):
            for observer, (prefix, iargs, ikw) in self.observers.iteritems():
                ikw = ikw.copy()
                ikw.update(kw)
                iargs = iargs+args
                handler = getattr(observer, prefix + name)
                try:
                    handler(*iargs, **ikw)
                except:
                    import traceback
                    traceback.print_stack()
                    print "Exception caught here:"
                    traceback.print_exc()
        return func
    notify = attrspace_property(get_notifier)
