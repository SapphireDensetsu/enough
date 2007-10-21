import nodes
from functools import partial

def ccode_widget_for(x):
    # TODO TEMP CODE
    from gui.TextEdit import TextEdit
    from ccode import CCodeGenerator
    c = CCodeGenerator()
    return TextEdit(partial(c.ccode, x))
    

def cached_widget_for(items):
    return CacheMap(widget_for, List(items))


def tabbed(widget):
    from gui.Box import HBox
    from List import List
    b = HBox(List([widget_for(' '), widget]))
    b.is_centered = True
    b.frame_color = None
    return b


def widget_for(x):
    # TODO: Circular import must be inside, yuck, how to fix?

    if isinstance(x, nodes.Module):
        from ModuleWidget import ModuleWidget
        return ModuleWidget(x)
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
    elif isinstance(x, nodes.Ptr):
        from PtrTypeWidget import PtrTypeWidget
        return PtrTypeWidget(x)
    elif isinstance(x, nodes.Array):
        from ArrayTypeWidget import ArrayTypeWidget
        return ArrayTypeWidget(x)


    elif isinstance(x, nodes.If):
        from IfWidget import IfWidget
        return IfWidget(x)

    elif isinstance(x, nodes.Equals):
        from BinaryOpWidget import EqualsWidget
        return EqualsWidget(x)
    elif isinstance(x, nodes.NotEquals):
        from BinaryOpWidget import NotEqualsWidget
        return NotEqualsWidget(x)
    elif isinstance(x, nodes.Assign):
        from BinaryOpWidget import AssignWidget
        return AssignWidget(x)
    elif isinstance(x, nodes.Subtract):
        from BinaryOpWidget import SubtractWidget
        return SubtractWidget(x)
    
    elif isinstance(x, str):
        # If it is a pythonic string, just make a text edit
        from gui.TextEdit import TextEdit
        return TextEdit(lambda : x)
        
    else:
        return ccode_widget_for(x)
        #assert False, "Don't know how to widget %r" % (x,)
