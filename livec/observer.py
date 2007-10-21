def observed_method(name=None):
    def decorator(func):
        if name is None:
            oname = func.__name__
        from functools import wraps
        @wraps(func)
        def new_func(self, *args, **kw):
            result = func(self, *args, **kw)
            for observer in self.observers:
                handler = getattr(observer, 'observe_' + oname, None)
                if handler is not None:
                    handler(*args, **kw)
            return result
        return new_func
    return decorator

# TODO: When do we remove_observer? Use weakref?
class Observable(object):
    def __init__(self):
        self.observers = []
    def add_observer(self, observer):
        self.observers.append(observer)
    def remove_observer(self, observer):
        self.observers.remove(observer)
