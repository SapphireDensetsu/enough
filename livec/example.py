from SlotClass import SlotClass

class BuiltinType(SlotClass):
    __slots__ = ['name', 'meta']
    defaults = dict(meta=dict)

class Variable(SlotClass):
    __slots__ = ['type', 'meta']
    defaults = dict(meta=dict)

class Ptr(SlotClass):
    __slots__ = ['pointed_type', 'meta']
    defaults = dict(meta=dict)

class Define(SlotClass):
    __slots__ = ['expr', 'meta']
    defaults = dict(meta=dict)

class Enum(SlotClass):
    __slots__ = ['values', 'meta']
    defaults = dict(meta=dict)

class EnumValue(SlotClass):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)

class Import(SlotClass):
    __slots__ = ['include', 'name', 'meta']
    defaults = dict(meta=dict)

class ArrayDeref(SlotClass):
    __slots__ = ['expr', 'index', 'meta']
    defaults = dict(meta=dict)

class Subtract(SlotClass):
    __slots__ = ['lexpr', 'rexpr', 'meta']
    defaults = dict(meta=dict)
 
class LiteralInt(SlotClass):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)

class LiteralString(SlotClass):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)

class LiteralChar(SlotClass):
    __slots__ = ['value', 'meta']
    defaults = dict(meta=dict)

class Module(SlotClass):
    __slots__ = ['defines', 'types', 'variable_declarations', 'functions', 'meta']
    defaults = dict(meta=dict, defines=list, types=list,
                    variable_declarations=list, functions=list)

class Function(SlotClass):
    __slots__ = ['return_type', 'parameters', 'block', 'meta']
    defaults = dict(meta=dict)

class Block(SlotClass):
    __slots__ = ['statements', 'variable_declarations', 'meta']
    defaults = dict(meta=dict, variable_declarations=list)

class If(SlotClass):
    __slots__ = ['expr', 'then', 'meta']
    defaults = dict(meta=dict)

class NotEquals(SlotClass):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=dict)

class Equals(SlotClass):
    __slots__ = ['a', 'b', 'meta']
    defaults = dict(meta=dict)

class Return(SlotClass):
    __slots__ = ['expr', 'meta']
    defaults = dict(meta=dict)

class Assign(SlotClass):
    __slots__ = ['lvalue', 'rvalue', 'meta']
    defaults = dict(meta=dict)

class Call(SlotClass):
    __slots__ = ['func', 'args', 'meta']
    defaults = dict(meta=dict)

int = BuiltinType(name='int')
char = BuiltinType(name='char')

argc=Variable(meta=dict(name='argc'), type=int)
argv=Variable(meta=dict(name='argv'), type=Ptr(pointed_type=
                                               Ptr(pointed_type=char)))

arg_count = Define(meta=dict(name='ARG_COUNT'), expr=LiteralInt(value=2))
ok = EnumValue(meta=dict(name='OK'), value=LiteralInt(value=0))
error = EnumValue(meta=dict(name='ERROR'), value=LiteralInt(value=1))
s = Variable(meta=dict(name='s'), type=Ptr(pointed_type=char))
strchr = Import(include='string.h', name='strchr')
fprintf = Import(include='stdio.h', name='fprintf')
printf = Import(include='stdio.h', name='printf')
stderr = Import(include='stdio.h', name='stderr')
null = Import(include='stddef.h', name='NULL')

argv_1 = ArrayDeref(expr=argv, index=1)

example = Module(
    meta=dict(name='example.c'),
    defines=[arg_count],
    types=[Enum(meta=dict(name='return_value'),
                values=[ok, error])],
    functions=[
        Function(meta=dict(name='main'), return_type=int,
                 parameters=[argc, argv],
                 block=Block(
                     variable_declarations=[s],
                     statements=[
                         If(expr=NotEquals(arg_count, argc),
                            then=Block(statements=[
                                Return(expr=error),
                            ])
                         ),
                         Assign(lvalue=s,
                                rvalue=Call(strchr, args=[argv_1, LiteralChar(value=',')])),
                         If(expr=Equals(null, s),
                            then=Block(statements=[
                                Call(fprintf, args=[stderr, LiteralString("No comma!\n")]),
                                Return(expr=error),
                            ])
                         ),
                         Call(printf, args=[LiteralString("Your comma is at %d!\n"),
                                            Subtract(s, argv_1)]),
                         Return(expr=ok)
                     ]
                 )
        )
    ]
)
