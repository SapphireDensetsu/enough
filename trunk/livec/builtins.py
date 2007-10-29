# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

# TODO: This is c-specific
import nodes
from lib.observable.ValueContainer import ValueContainer
from functools import partial

def builtin_type(name):
    return partial(ValueContainer,
                   nodes.BuiltinType(name=name, meta=nodes.Meta(name=name)))

def import_(include, name):
    return partial(ValueContainer,
                   nodes.Import(include=include, name=name, meta=nodes.Meta(name=name)))

int = builtin_type('int')
char = builtin_type('char')

strchr = import_(include='<string.h>', name='strchr')
fprintf = import_(include='<stdio.h>', name='fprintf')
printf = import_(include='<stdio.h>', name='printf')
stderr = import_(include='<stdio.h>', name='stderr')
null = import_(include='<stddef.h>', name='NULL')
