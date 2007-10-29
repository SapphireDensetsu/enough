# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import nodes
import builtins
from lib.observable.List import List
from lib.observable.ValueContainer import ValueContainer
from functools import partial

argc = partial(ValueContainer,
               nodes.Variable(meta=nodes.Meta(name='argc'), type=builtins.int()))

argv = partial(ValueContainer,
               nodes.Variable(meta=nodes.Meta(name='argv'),
                              type=nodes.Ptr.proxy(pointed_type=
                                                   nodes.Ptr.proxy(pointed_type=builtins.char()))))

arg_count = partial(ValueContainer,
                    nodes.Define(meta=nodes.Meta(name='ARG_COUNT'),
                                 expr=nodes.LiteralInt.proxy(value=2)))

_ret_value = nodes.Enum(meta=nodes.Meta(name='ret_value'))
ret_value = partial(ValueContainer, _ret_value)

ok = partial(ValueContainer,
             nodes.EnumValue(meta=nodes.Meta(name='OK'),
                             value=nodes.LiteralInt.proxy(value=0),
                             enum=ret_value()))
_ret_value.values.append(ok())

error = partial(ValueContainer,
                nodes.EnumValue(meta=nodes.Meta(name='ERROR'),
                                value=nodes.LiteralInt.proxy(value=1),
                                enum=ret_value()))
_ret_value.values.append(error())

char_variable = partial(ValueContainer,
                        nodes.Variable(type=nodes.Ptr.proxy(pointed_type=builtins.char())))

def argv_1():
    return nodes.ArrayDeref.proxy(expr=argv(), index=nodes.LiteralInt.proxy(value=1))

example = nodes.Module.proxy(
    meta=nodes.Meta(name='example.c'),
    declarations=List([
        nodes.Function.proxy(
            meta=nodes.Meta(name='main'),
            type=nodes.FunctionType.proxy(return_type=builtins.int(),
                                          parameters=List([argc(), argv()])),
            block=nodes.Block.proxy(statements=List([
                nodes.If.proxy(expr=nodes.NotEquals.proxy(arg_count(), argc()),
                               if_true=nodes.Block.proxy(statements=List([nodes.Return.proxy(expr=error())]))),
                nodes.Assign.proxy(lvalue=char_variable(),
                                   rvalue=nodes.Call.proxy(builtins.strchr(), args=List([argv_1(), nodes.LiteralChar.proxy(value=',')]))),
                nodes.If.proxy(expr=nodes.Equals.proxy(builtins.null(), char_variable()),
                               if_true=nodes.Block.proxy(statements=List([
                       nodes.Call.proxy(builtins.fprintf(),
                                        args=List([builtins.stderr(),
                                                   nodes.LiteralString.proxy("No comma!\n")])),
                       nodes.Return.proxy(expr=error()),
                   ]))
                ),
                nodes.Call.proxy(builtins.printf(),
                                 args=List([nodes.LiteralString.proxy("Your comma is at %d!\n"),
                                            nodes.Subtract.proxy(char_variable(), argv_1())])),
                nodes.Return.proxy(expr=ok())
            ]))
        )
    ])
)
