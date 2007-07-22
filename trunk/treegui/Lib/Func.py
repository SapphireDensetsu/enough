def cached(func):
    results = {}
    def new_func(*args, **kw):
        if kw:
            return func(*args, **kw)
        
        if args not in results:
            results[args] = func(*args, **kw)
        return results[args]
    return new_func

