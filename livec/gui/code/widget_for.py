import nodes

def widget_for(x):
    # TODO: Circular import must be inside, yuck, how to fix?
    from ModuleWidget import ModuleWidget
    from MetaWidget import MetaWidget
    from FunctionWidget import FunctionWidget
    if isinstance(x, nodes.Module):
        return ModuleWidget(x)
    elif isinstance(x, nodes.Meta):
        return MetaWidget(x)
    elif isinstance(x, nodes.Function):
        return FunctionWidget(x)
    elif isinstance(x, nodes.BuiltinType):
        return MetaWidget(x.meta)
    else:
        assert False, "Don't know how to widget %r" % (x,)
