# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import itertools
from lib.SlotClass import SlotClass

from lib.observer import Observable
from lib.proxyclass import proxy_class

from lib.observable.List import List

class Meta(dict):
    """This is a special kind of node that does not affect the
    semantics in any way, and only useful for the petty human. This is
    why it does not inherit from Node, and is not included in the
    referred() graph."""
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)
        self.obs_dict = Observable()


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
    __slots__ = ['type', 'block', 'meta']
    defaults = dict(meta=Meta)
    def referred(self):
        yield self.type
        yield self.block

class FunctionType(Node):
    __slots__ = ['meta', 'return_type', 'parameters']
    defaults = dict(meta=Meta)
    def referred(self):
        yield self.return_type
        for param in self.parameters:
            yield param

class BuiltinType(Node):
    __slots__ = ['name', 'meta']
    defaults = dict(meta=Meta)

class Ptr(Node):
    __slots__ = ['pointed_type', 'meta']
    defaults = dict(meta=Meta)

class Array(Node):
    # TODO these are constant-sized arrays. what about [] array types?
    __slots__ = ['element_type', 'size', 'meta']
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

class DeclarationsContainer(Node):
    __slots__ = ['declarations']

class Module(DeclarationsContainer):
    __slots__ = DeclarationsContainer.__slots__ + ['meta']
    defaults = dict(declarations=List, meta=Meta)
    def referred(self):
        return itertools.chain(self.declarations)

class Block(DeclarationsContainer):
    __slots__ = ['statements'] + DeclarationsContainer.__slots__ + ['meta']
    defaults = dict(declarations=List, meta=Meta)
    def referred(self):
        return self.statements

class NotEquals(Node):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=Meta)

class Equals(Node):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=Meta)

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
