def cached(func):
    results = {}
    def new_func(*args, **kw):
        if kw:
            return func(*args, **kw)
        
        if args not in results:
            results[args] = func(*args, **kw)
        return results[args]
    return new_func

class BoundFunc(object):
    def __init__(self, _callable, *args, **kw):
        self._callable = _callable
        self.args = args
        self.kw = kw
        
    def __call__(self, *args, **kw):
        # todo check overwriting of keys!
        all_kw = self.kw.copy()
        all_kw.update(kw)
        return self._callable(*(self.args + args), **all_kw)
    

