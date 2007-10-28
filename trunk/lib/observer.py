# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from lib.Space import attrspace_property

import weakref

class Observable(object):
    def __init__(self):
        self.observers = weakref.WeakKeyDictionary()

    def __getstate__(self):
        d = self.__dict__.copy()
        oldobs = d['observers']
        newobs = {}
        for k,v in oldobs.items():
            newobs[k] = v
        d['observers'] = newobs
        return d
    def __setstate__(self, d):
        d['observers'] = weakref.WeakKeyDictionary(d['observers'])
        for k,v in d.iteritems():
            self.__dict__[k] = v
    # It may be desirable in the future to have add_strong_observer
    # too that does keep observer alive.

    def add_observer(self, observer, prefix, *args, **kw):
        """Adds the given observer to this observable.

        The observer will be notified of events by calling its methods
        prefixed by the given prefix (suffix is the event
        identifier). The given args are prepended to the event args,
        and the given kw are added to the event keywords.

        Note: The observer is weakly referenced. It is likely
        desirable that given args/kw are also not strong references."""
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
