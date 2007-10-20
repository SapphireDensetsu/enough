import nodes

def widget_for(x):
    # TODO: Circular import must be inside, yuck, how to fix?
    from ModuleWidget import ModuleWidget
    from MetaWidget import MetaWidget
    if isinstance(x, nodes.Module):
        return ModuleWidget(x)
    elif isinstance(x, nodes.Meta):
        return MetaWidget(x)
    else:
        assert False, "Don't know how to widget %r" % (x,)