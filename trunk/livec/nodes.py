import itertools
from SlotClass import SlotClass

from observer import Observable, observed_method
from proxyclass import proxy_class

class Meta(Observable):
    """This is a special kind of node that does not affect the
    semantics in any way, and only useful for the petty human. This is
    why it does not inherit from Node, and is not included in the
    referred() graph."""
    def __init__(self, *args, **kw):
        self._dict = dict(*args, **kw)
        Observable.__init__(self)

Meta = proxy_class(Meta, '_dict', methods=[
    '__iter__',
    '__getitem__',
    '__len__',
    'iterkeys',
    'iteritems',
    'itervalues',
    'keys',
    'items',
    'values',
])

class List(Observable):
    def __init__(self, *args, **kw):
        Observable.__init__(self)
        self._items = list(*args, **kw)

    @observed_method()
    def insert(self, index, item):
        self._items.insert(index, item)
    
    @observed_method()
    def remove(self, item):
        self._items.remove(item)


    def append(self, item):
        self.insert(len(self), item)
List = proxy_class(List, '_items', methods=[
    '__getitem__',
    '__len__',
])

class Node(SlotClass):
    def referred(self):
        for i in self.__slots__:
            x = getattr(self, i)
            if isinstance(x, Node):
                yield x

class Named(Node):
    def __init__(self, *args, **kw):
        Node.__init__(self, *args, **kw)

class Variable(Named):
    __slots__ = ['type', 'meta']
    defaults = dict(meta=Meta)

class Define(Named):
    __slots__ = ['expr', 'meta']
    defaults = dict(meta=Meta)

class Enum(Named):
    __slots__ = ['meta', 'values']
    defaults = dict(meta=Meta, values=List)
    def referred(self):
        return self.values

class EnumValue(Named):
    __slots__ = ['value', 'enum', 'meta']
    defaults = dict(meta=Meta)

class Function(Named):
    __slots__ = ['return_type', 'parameters', 'block', 'meta']
    defaults = dict(meta=Meta)
    def referred(self):
        yield self.return_type
        for param in self.parameters:
            yield param
        yield self.block

class BuiltinType(Node):
    __slots__ = ['name', 'meta']
    defaults = dict(meta=Meta)

class Ptr(Node):
    __slots__ = ['pointed_type', 'meta']
    defaults = dict(meta=Meta)

class Declaration(Node):
    __slots__ = ['obj']

class Import(Node):
    __slots__ = ['include', 'name', 'meta']
    defaults = dict(meta=Meta)

class ArrayDeref(Node):
    __slots__ = ['expr', 'index', 'meta']
    defaults = dict(meta=Meta)

class Subtract(Node):
    __slots__ = ['lexpr', 'rexpr', 'meta']
    defaults = dict(meta=Meta)
 
class LiteralInt(Node):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=Meta)

class LiteralString(Node):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=Meta)

class LiteralChar(Node):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=Meta)

class Module(Node):
    __slots__ = ['functions', 'variables', 'meta']
    defaults = dict(meta=Meta, functions=List, variables=List)
    def referred(self):
        return itertools.chain(self.functions, self.variables)

class NotEquals(Node):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=Meta)

class Equals(Node):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=Meta)

class Block(Node):
    __slots__ = ['statements', 'meta']
    defaults = dict(meta=Meta)
    def referred(self):
        return self.statements

class If(Node):
    __slots__ = ['expr', 'if_true', 'if_false', 'meta']
    defaults = dict(meta=Meta, if_false=lambda: None)

class Return(Node):
    __slots__ = ['expr', 'meta']
    defaults = dict(meta=Meta)

class Assign(Node):
    __slots__ = ['lvalue', 'rvalue', 'meta']
    defaults = dict(meta=Meta)

class Call(Node):
    __slots__ = ['func', 'args', 'meta']
    defaults = dict(meta=Meta)
    def referred(self):
        yield self.func
        for arg in self.args:
            yield arg
