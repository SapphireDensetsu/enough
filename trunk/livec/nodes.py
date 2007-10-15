import itertools
from SlotClass import SlotClass

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
    defaults = dict(meta=dict)

class Define(Named):
    __slots__ = ['expr', 'meta']
    defaults = dict(meta=dict)

class Enum(Named):
    __slots__ = ['meta', 'values']
    defaults = dict(meta=dict, values=list)
    def referred(self):
        return self.values

class EnumValue(Named):
    __slots__ = ['value', 'enum', 'meta']
    defaults = dict(meta=dict)

class Function(Named):
    __slots__ = ['return_type', 'parameters', 'block', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.return_type
        for param in self.parameters:
            yield param
        yield self.block

class BuiltinType(Node):
    __slots__ = ['name', 'meta']
    defaults = dict(meta=dict)

class Ptr(Node):
    __slots__ = ['pointed_type', 'meta']
    defaults = dict(meta=dict)

class Declaration(Node):
    __slots__ = ['obj']

class Import(Node):
    __slots__ = ['include', 'name', 'meta']
    defaults = dict(meta=dict)

class ArrayDeref(Node):
    __slots__ = ['expr', 'index', 'meta']
    defaults = dict(meta=dict)

class Subtract(Node):
    __slots__ = ['lexpr', 'rexpr', 'meta']
    defaults = dict(meta=dict)
 
class LiteralInt(Node):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)

class LiteralString(Node):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)
    # TODO: To ccode
    def _c_escape(self, value):
        return value.replace('\\', '\\\\').replace('\n', '\\n')

class LiteralChar(Node):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)

class Module(Node):
    __slots__ = ['functions', 'variables', 'meta']
    defaults = dict(meta=dict, functions=list, variables=list)
    def referred(self):
        return itertools.chain(self.functions, self.variables)

class NotEquals(Node):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=dict)

class Equals(Node):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=dict)

class Block(Node):
    __slots__ = ['statements', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        return self.statements

class If(Node):
    __slots__ = ['expr', 'if_true', 'if_false', 'meta']
    defaults = dict(meta=dict, if_false=lambda: None)

class Return(Node):
    __slots__ = ['expr', 'meta']
    defaults = dict(meta=dict)

class Assign(Node):
    __slots__ = ['lvalue', 'rvalue', 'meta']
    defaults = dict(meta=dict)

class Call(Node):
    __slots__ = ['func', 'args', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.func
        for arg in self.args:
            yield arg
