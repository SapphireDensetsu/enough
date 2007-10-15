import ccode
import nodes

int = nodes.BuiltinType(name='int')
char = nodes.BuiltinType(name='char')

argc=nodes.Variable(meta=dict(name='argc'), type=int)
argv=nodes.Variable(meta=dict(name='argv'), type=nodes.Ptr(pointed_type=
                                               nodes.Ptr(pointed_type=char)))

arg_count = nodes.Define(meta=dict(name='ARG_COUNT'), expr=nodes.LiteralInt(value=2))

ret_value = nodes.Enum(meta=dict(name='ret_value'))
ok = nodes.EnumValue(meta=dict(name='OK'), value=nodes.LiteralInt(value=0), enum=ret_value)
ret_value.values.append(ok)
error = nodes.EnumValue(meta=dict(name='ERROR'), value=nodes.LiteralInt(value=1), enum=ret_value)
ret_value.values.append(error)

s = nodes.Variable(meta=dict(), type=nodes.Ptr(pointed_type=char))
strchr = nodes.Import(include='<string.h>', name='strchr')
fprintf = nodes.Import(include='<stdio.h>', name='fprintf')
printf = nodes.Import(include='<stdio.h>', name='printf')
stderr = nodes.Import(include='<stdio.h>', name='stderr')
null = nodes.Import(include='<stddef.h>', name='NULL')

argv_1 = nodes.ArrayDeref(expr=argv, index=nodes.LiteralInt(value=1))

example = nodes.Module(
    meta=dict(name='example.c'),
    functions=[
        nodes.Function(meta=dict(name='main'), return_type=int,
                       parameters=[argc, argv],
                       block=nodes.Block(
            statements=[
                nodes.If(expr=nodes.NotEquals(arg_count, argc),
                   if_true=nodes.Block(statements=[
                       nodes.Return(expr=error),
                   ])
                ),
                nodes.Assign(lvalue=s,
                       rvalue=nodes.Call(strchr, args=[argv_1, nodes.LiteralChar(value=',')])),
                nodes.If(expr=nodes.Equals(null, s),
                   if_true=nodes.Block(statements=[
                       nodes.Call(fprintf, args=[stderr, nodes.LiteralString("No comma!\n")]),
                       nodes.Return(expr=error),
                   ])
                ),
                nodes.Call(printf, args=[nodes.LiteralString("Your comma is at %d!\n"),
                                   nodes.Subtract(s, argv_1)]),
                nodes.Return(expr=ok)
                ]
            )
        )
    ]
)

g = ccode.CCodeGenerator()
open('example2.c','wb').write(g.ccode(example))
