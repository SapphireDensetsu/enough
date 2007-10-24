import nodes

int = nodes.BuiltinType(name='int', meta=nodes.Meta(name='int'))
char = nodes.BuiltinType(name='char', meta=nodes.Meta(name='char'))
void = nodes.BuiltinType(name='void', meta=nodes.Meta(name='void'))
strchr = nodes.Import(include='<string.h>', name='strchr', meta=nodes.Meta(name='strchr'))
fprintf = nodes.Import(include='<stdio.h>', name='fprintf', meta=nodes.Meta(name='fprintf'))
printf = nodes.Import(include='<stdio.h>', name='printf', meta=nodes.Meta(name='printf'))
stderr = nodes.Import(include='<stdio.h>', name='stderr', meta=nodes.Meta(name='stderr'))
null = nodes.Import(include='<stddef.h>', name='NULL', meta=nodes.Meta(name='NULL'))
