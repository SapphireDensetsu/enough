import nodes
from functools import partial

def ccode_widget_for(x):
    from gui.TextEdit import TextEdit
    from ccode import CCodeGenerator
    c = CCodeGenerator()
    return TextEdit(partial(c.ccode, x))
    
def widget_for(x):
    # TODO: Circular import must be inside, yuck, how to fix?
    from gui.TextEdit import TextEdit

    from ModuleWidget import ModuleWidget
    from MetaWidget import MetaWidget
    from FunctionWidget import FunctionWidget
    from BuiltInTypeWidget import BuiltInTypeWidget
    from VariableWidget import VariableWidget
    from BlockWidget import BlockWidget
    
    if isinstance(x, nodes.Module):
        return ModuleWidget(x)
    elif isinstance(x, nodes.Meta):
        return MetaWidget(x)
    elif isinstance(x, nodes.Function):
        return FunctionWidget(x)
    elif isinstance(x, nodes.BuiltinType):
        return BuiltInTypeWidget(x)
    elif isinstance(x, nodes.Variable):
        return VariableWidget(x)
    elif isinstance(x, nodes.Block):
        return BlockWidget(x)
    else:
        assert False, "Don't know how to widget %r" % (x,)
