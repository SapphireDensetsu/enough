import itertools
from SlotClass import SlotClass

class BuiltinType(SlotClass):
    __slots__ = ['name', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        return []

class Ptr(SlotClass):
    __slots__ = ['pointed_type', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.pointed_type

class Named(SlotClass):
    def __init__(self, *args, **kw):
        SlotClass.__init__(self, *args, **kw)

class Declaration(SlotClass):
    __slots__ = ['obj']
    def referred(self):
        yield self.obj

class Variable(Named):
    __slots__ = ['type', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.type

class Define(Named):
    __slots__ = ['expr', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        return []

class Enum(Named):
    __slots__ = ['values', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        return self.values

class EnumValue(Named):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.value

class Import(SlotClass):
    __slots__ = ['include', 'name', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        return []

class ArrayDeref(SlotClass):
    __slots__ = ['expr', 'index', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.expr
        yield self.index

class Subtract(SlotClass):
    __slots__ = ['lexpr', 'rexpr', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.lexpr
        yield self.rexpr
 
class LiteralInt(SlotClass):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        return []

class LiteralString(SlotClass):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        return []
    def _c_escape(self, value):
        return value.replace('\\', '\\\\').replace('\n', '\\n')

class LiteralChar(SlotClass):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        return []

class Module(SlotClass):
    __slots__ = ['defines', 'types', 'variable_declarations', 'functions', 'meta']
    defaults = dict(meta=dict, defines=list, types=list,
                    variable_declarations=list, functions=list)
    def referred(self):
        return itertools.chain(
            self.defines,
            self.types,
            self.variable_declarations,
            self.functions
        )

class Function(Named):
    __slots__ = ['return_type', 'parameters', 'block', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.return_type
        for param in self.parameters:
            yield param
        yield self.block

class NotEquals(SlotClass):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.a
        yield self.b

class Equals(SlotClass):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.a
        yield self.b

class Block(SlotClass):
    __slots__ = ['statements', 'variable_declarations', 'meta']
    defaults = dict(meta=dict, variable_declarations=list)
    def referred(self):
        return itertools.chain(self.statements, self.variable_declarations)

class If(SlotClass):
    __slots__ = ['expr', 'if_true', 'if_false', 'meta']
    defaults = dict(meta=dict, if_false=lambda: None)
    def referred(self):
        yield self.expr
        yield self.if_true
        if self.if_false is not None:
            yield self.if_false

class Return(SlotClass):
    __slots__ = ['expr', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.expr

class Assign(SlotClass):
    __slots__ = ['lvalue', 'rvalue', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.lvalue
        yield self.rvalue

class Call(SlotClass):
    __slots__ = ['func', 'args', 'meta']
    defaults = dict(meta=dict)
    def referred(self):
        yield self.func
        for arg in self.args:
            yield arg
