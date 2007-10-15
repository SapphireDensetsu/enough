import itertools
from SlotClass import SlotClass

class Type:
    def c_declcode(self, name):
        return '%s %s' % (self.c_basetype(), self.c_posttype(name))

class BuiltinType(SlotClass, Type):
    __slots__ = ['name', 'meta']
    defaults = dict(meta=dict)
    def c_basetype(self):
        return self.name
    def c_posttype(self, name):
        return name
    def referred(self):
        return []

class Ptr(SlotClass, Type):
    __slots__ = ['pointed_type', 'meta']
    defaults = dict(meta=dict)
    def c_basetype(self):
        return self.pointed_type.c_basetype()
    def c_posttype(self, name):
        return '(*%s)' % (self.pointed_type.c_posttype(name),)
    def referred(self):
        yield self.pointed_type

def make_names():
    for i in itertools.count():
        yield 'name%d' % (i,)

names = make_names()

class Named(SlotClass):
    def __init__(self, *args, **kw):
        SlotClass.__init__(self, *args, **kw)
        if self.c_name is None:
            if 'name' in self.meta:
                self.c_name = self.meta['name']
            else:
                self.c_name = names.next()

class Declaration(SlotClass):
    __slots__ = ['obj']
    def c_code(self):
        return self.obj.c_declcode()
    def referred(self):
        yield self.obj

class Variable(Named):
    __slots__ = ['type', 'meta', 'c_name']
    defaults = dict(meta=dict, c_name=lambda : None)
    def c_code(self):
        return self.c_name
    def c_declcode(self):
        return self.type.c_declcode(self.c_name)
    def referred(self):
        yield self.type

class Define(Named):
    __slots__ = ['expr', 'meta', 'c_name']
    defaults = dict(meta=dict, c_name=lambda : None)
    def c_declcode(self):
        return '#define %s %s' % (self.c_name, self.expr.c_code())
    def c_code(self):
        return self.c_name
    def referred(self):
        return []

class Enum(Named):
    __slots__ = ['values', 'meta', 'c_name']
    defaults = dict(meta=dict, c_name=lambda : None)
    def c_declcode(self):
        return 'enum %s {%s};' % (
            self.c_name, ', '.join('%s=%s' % (value.c_name, value.value.c_code())
                                   for value in self.values))
    def referred(self):
        return self.values

class EnumValue(Named):
    __slots__ = ['value', 'meta', 'c_name']
    defaults = dict(meta=dict, c_name=lambda : None)
    def c_code(self):
        return self.c_name
    def referred(self):
        yield self.value

class Import(SlotClass):
    __slots__ = ['include', 'name', 'meta']
    defaults = dict(meta=dict)
    def c_code(self):
        return self.name
    def referred(self):
        return []

class ArrayDeref(SlotClass):
    __slots__ = ['expr', 'index', 'meta']
    defaults = dict(meta=dict)
    def c_code(self):
        return '(%s[%s])' % (self.expr.c_code(), self.index.c_code())
    def referred(self):
        yield self.expr
        yield self.index

class Subtract(SlotClass):
    __slots__ = ['lexpr', 'rexpr', 'meta']
    defaults = dict(meta=dict)
    def c_code(self):
        return '(%s-%s)' % (self.lexpr.c_code(), self.rexpr.c_code())
    def referred(self):
        yield self.lexpr
        yield self.rexpr
 
class LiteralInt(SlotClass):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)
    def c_code(self):
        return str(self.value)
    def referred(self):
        return []

class LiteralString(SlotClass):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)
    def c_code(self):
        return '"%s"' % self._c_escape(self.value,)
    def referred(self):
        return []
    def _c_escape(self, value):
        return value.replace('\\', '\\\\').replace('\n', '\\n')

class LiteralChar(SlotClass):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)
    def c_code(self):
        return "'%c'" % (self.value,)
    def referred(self):
        return []

import functools

def concat_lines(func):
    @functools.wraps(func)
    def new_func(*args, **kw):
        return '\n'.join(func(*args, **kw)) + '\n'
    return new_func

class Module(SlotClass):
    __slots__ = ['defines', 'types', 'variable_declarations', 'functions', 'meta']
    defaults = dict(meta=dict, defines=list, types=list,
                    variable_declarations=list, functions=list)
    @concat_lines
    def c_code(self):
        for x in self._includes():
            yield '#include %s' % (x,)
        for x in self.defines:
            yield x.c_code()
        for x in self.types:
            yield x.c_code() + ';'
        for x in self.variable_declarations:
            yield x.c_code() + ';'
        for x in self.functions:
            yield x.c_code()
    def referred(self):
        return itertools.chain(
            self.defines,
            self.types,
            self.variable_declarations,
            self.functions
        )
    def _includes(self):
        i = set()
        for x in visit_all(self):
            if isinstance(x, Import):
                i.add(x.include)
        return i

def visit_all(x, visited=None):
    if visited is None:
        visited = set()
    visited.add(x)
    yield x
    for i in x.referred():
        if i in visited:
            continue
        for x in visit_all(i, visited):
            yield x

class Function(Named):
    __slots__ = ['return_type', 'parameters', 'block', 'meta', 'c_name']
    defaults = dict(meta=dict, c_name=lambda : None)
    @concat_lines
    def c_declcode(self):
        yield '%s(%s)' % (self.return_type.c_declcode(self.c_name),
                          ', '.join(param.c_code()
                                    for param in self.parameters))
        yield '{'
        yield self.block.c_code()
        yield '}'
    def referred(self):
        yield self.return_type
        for param in self.parameters:
            yield param
        yield self.block

class Block(SlotClass):
    __slots__ = ['statements', 'variable_declarations', 'meta']
    defaults = dict(meta=dict, variable_declarations=list)
    @concat_lines
    def c_code(self):
        yield '{'
        for variable_declaration in self.variable_declarations:
            yield variable_declaration.c_code() + ';'
        for statement in self.statements:
            yield statement.c_code() + ';'
        yield '}'
    def referred(self):
        return itertools.chain(self.statements, self.variable_declarations)

class If(SlotClass):
    __slots__ = ['expr', 'if_true', 'if_false', 'meta']
    defaults = dict(meta=dict, if_false=lambda: None)
    @concat_lines
    def c_code(self):
        yield 'if(%s)' % (self.expr.c_code(),)
        yield '{'
        yield self.if_true.c_code()
        yield '}'
        if self.if_false is not None:
            yield 'else'
            yield '{'
            yield self.if_false.c_code()
            yield '}'
    def referred(self):
        yield self.expr
        yield self.if_true
        if self.if_false is not None:
            yield self.if_false

class NotEquals(SlotClass):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=dict)
    def c_code(self):
        return '(%s!=%s)' % (self.a.c_code(), self.b.c_code())
    def referred(self):
        yield self.a
        yield self.b

class Equals(SlotClass):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=dict)
    def c_code(self):
        return '(%s==%s)' % (self.a.c_code(), self.b.c_code())
    def referred(self):
        yield self.a
        yield self.b

class Return(SlotClass):
    __slots__ = ['expr', 'meta']
    defaults = dict(meta=dict)
    def c_code(self):
        return 'return %s' % (self.expr.c_code(),)
    def referred(self):
        yield self.expr

class Assign(SlotClass):
    __slots__ = ['lvalue', 'rvalue', 'meta']
    defaults = dict(meta=dict)
    def c_code(self):
        return '(%s=%s)' % (self.lvalue.c_code(), self.rvalue.c_code())
    def referred(self):
        yield self.lvalue
        yield self.rvalue

class Call(SlotClass):
    __slots__ = ['func', 'args', 'meta']
    defaults = dict(meta=dict)
    def c_code(self):
        return '(%s(%s))' % (self.func.c_code(), ','.join(arg.c_code()
                                                          for arg in self.args))
    def referred(self):
        yield self.func
        for arg in self.args:
            yield arg

int = BuiltinType(name='int')
char = BuiltinType(name='char')

argc=Variable(meta=dict(name='argc'), type=int)
argv=Variable(meta=dict(name='argv'), type=Ptr(pointed_type=
                                               Ptr(pointed_type=char)))

arg_count = Define(meta=dict(name='ARG_COUNT'), expr=LiteralInt(value=2))
ok = EnumValue(meta=dict(name='OK'), value=LiteralInt(value=0))
error = EnumValue(meta=dict(name='ERROR'), value=LiteralInt(value=1))
s = Variable(meta=dict(name='s'), type=Ptr(pointed_type=char))
strchr = Import(include='<string.h>', name='strchr')
fprintf = Import(include='<stdio.h>', name='fprintf')
printf = Import(include='<stdio.h>', name='printf')
stderr = Import(include='<stdio.h>', name='stderr')
null = Import(include='<stddef.h>', name='NULL')

argv_1 = ArrayDeref(expr=argv, index=LiteralInt(value=1))

example = Module(
    meta=dict(name='example.c'),
    defines=[Declaration(arg_count)],
    types=[Declaration(Enum(meta=dict(name='return_value'),
                            values=[ok, error]))],
    functions=[
        Declaration(Function(meta=dict(name='main'), return_type=int,
                             parameters=[Declaration(argc),
                                         Declaration(argv)],
                             block=Block(
            variable_declarations=[Declaration(s)],
            statements=[
                If(expr=NotEquals(arg_count, argc),
                   if_true=Block(statements=[
                       Return(expr=error),
                   ])
                ),
                Assign(lvalue=s,
                       rvalue=Call(strchr, args=[argv_1, LiteralChar(value=',')])),
                If(expr=Equals(null, s),
                   if_true=Block(statements=[
                       Call(fprintf, args=[stderr, LiteralString("No comma!\n")]),
                       Return(expr=error),
                   ])
                ),
                Call(printf, args=[LiteralString("Your comma is at %d!\n"),
                                   Subtract(s, argv_1)]),
                Return(expr=ok)
                ]
            )
        ))
    ]
)

open('example2.c','wb').write(example.c_code())
