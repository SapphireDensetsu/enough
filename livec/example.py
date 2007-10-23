import nodes
import builtins
from lib.observable.List import List


argc=nodes.Variable(meta=nodes.Meta(name='argc'), type=builtins.int)
argv=nodes.Variable(meta=nodes.Meta(name='argv'), type=nodes.Ptr(pointed_type=
                                               nodes.Ptr(pointed_type=builtins.char)))

arg_count = nodes.Define(meta=nodes.Meta(name='ARG_COUNT'), expr=nodes.LiteralInt(value=2))

ret_value = nodes.Enum(meta=nodes.Meta(name='ret_value'))
ok = nodes.EnumValue(meta=nodes.Meta(name='OK'), value=nodes.LiteralInt(value=0), enum=ret_value)
ret_value.values.append(ok)
error = nodes.EnumValue(meta=nodes.Meta(name='ERROR'), value=nodes.LiteralInt(value=1), enum=ret_value)
ret_value.values.append(error)

s = nodes.Variable(type=nodes.Ptr(pointed_type=builtins.char))
strchr = nodes.Import(include='<string.h>', name='strchr', meta=nodes.Meta(name='strchr'))
fprintf = nodes.Import(include='<stdio.h>', name='fprintf', meta=nodes.Meta(name='fprintf'))
printf = nodes.Import(include='<stdio.h>', name='printf', meta=nodes.Meta(name='printf'))
stderr = nodes.Import(include='<stdio.h>', name='stderr', meta=nodes.Meta(name='stderr'))
null = nodes.Import(include='<stddef.h>', name='NULL', meta=nodes.Meta(name='NULL'))

argv_1 = nodes.ArrayDeref(expr=argv, index=nodes.LiteralInt(value=1))

example = nodes.Module(
    meta=nodes.Meta(name='example.c'),
    functions=List([
        nodes.Function(
            meta=nodes.Meta(name='main'),
            type=nodes.FunctionType(return_type=builtins.int,
                                    parameters=List([argc, argv])),
            block=nodes.Block(statements=List([
                nodes.If(expr=nodes.NotEquals(arg_count, argc),
                         if_true=nodes.Block(statements=List([
                    nodes.Return(expr=error),
                ]))),
                nodes.Assign(lvalue=s,
                             rvalue=nodes.Call(strchr, args=List([argv_1, nodes.LiteralChar(value=',')]))),
                nodes.If(expr=nodes.Equals(null, s),
                   if_true=nodes.Block(statements=List([
                       nodes.Call(fprintf, args=List([stderr, nodes.LiteralString("No comma!\n")])),
                       nodes.Return(expr=error),
                   ]))
                ),
                nodes.Call(printf, args=List([nodes.LiteralString("Your comma is at %d!\n"),
                                              nodes.Subtract(s, argv_1)])),
                nodes.Return(expr=ok)
            ]))
        )
    ])
)
