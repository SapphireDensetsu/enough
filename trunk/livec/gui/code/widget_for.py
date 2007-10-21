import nodes
from functools import partial

def ccode_widget_for(x):
    from gui.TextEdit import TextEdit
    from ccode import CCodeGenerator
    c = CCodeGenerator()
    return TextEdit(partial(c.ccode, x))
    
def widget_for(x):
    # TODO: Circular import must be inside, yuck, how to fix?

    if isinstance(x, nodes.Module):
        from ModuleWidget import ModuleWidget
        return ModuleWidget(x)
    elif isinstance(x, nodes.Meta):
        from MetaWidget import MetaWidget
        return MetaWidget(x)
    elif isinstance(x, nodes.Function):
        from FunctionWidget import FunctionWidget
        return FunctionWidget(x)
    elif isinstance(x, nodes.BuiltinType):
        from BuiltInTypeWidget import BuiltInTypeWidget
        return BuiltInTypeWidget(x)
    elif isinstance(x, nodes.Variable):
        from VariableWidget import VariableWidget
        return VariableWidget(x)
    elif isinstance(x, nodes.Block):
        from BlockWidget import BlockWidget
        return BlockWidget(x)
    else:
        assert False, "Don't know how to widget %r" % (x,)
