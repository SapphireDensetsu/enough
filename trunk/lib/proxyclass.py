# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

def proxy_method(name, attrname):
    def proxy(self, *args, **kw):
        realobj = getattr(self, attrname)
        realmethod = getattr(realobj, name)
        return realmethod(*args, **kw)
    return proxy

def proxy_class(cls, attrname, methods):
    """Add the given methods to the given class, implemented as
    proxies that forward the call to the object referenced by the
    given attribute name."""
    for name in methods:
        setattr(cls, name, proxy_method(name, attrname))
    return cls
