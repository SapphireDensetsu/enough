import nodes
from functools import partial
from gui.code import style

from gui.Box import HBox
from List import List

def ccode_widget_for(x):
    # TODO TEMP CODE
    from gui.TextEdit import TextEdit
    from ccode import CCodeGenerator
    c = CCodeGenerator()
    return TextEdit(partial(c.ccode, x))
    

def indented(widget):
    from gui.Spacer import Spacer
    b = HBox(List([Spacer((style.indent_width, 0)), widget]))
    b.is_centered = True
    b.frame_color = None
    return b

def posttype_widget_for(x, name):
    if isinstance(x, nodes.BuiltinType):
        from gui.TextEdit import make_label
        return make_label(name, color=style.identifier_color)
    elif isinstance(x, nodes.Ptr):
        from PtrTypeWidget import PtrTypeWidget
        return PtrTypeWidget(x, name)
    elif isinstance(x, nodes.Array):
        from ArrayTypeWidget import ArrayTypeWidget
        return ArrayTypeWidget(x, name)
    # TODO: Function-type (not function + body declaration, but
    # function type)
    else:
        assert False

def find_basetype(x):
    if isinstance(x, nodes.BuiltinType):
        return x
    elif isinstance(x, nodes.Ptr):
        return find_basetype(x.pointed_type)
    elif isinstance(x, nodes.Array):
        return find_basetype(x.element_type)
    else:
        assert False, "Cannot find base type of %r" % (x,)

def type_widget_for(x, name=''):
    from BuiltInTypeWidget import BuiltInTypeWidget
    basetype_widget = BuiltInTypeWidget(find_basetype(x))

    type_widget = HBox(List([
        basetype_widget,
        posttype_widget_for(x, name),
    ]))
    type_widget.is_centered = True
    return type_widget

def declaration_widget_for(x):
    if isinstance(x, nodes.Variable):
        from VariableDeclarationWidget import VariableDeclarationWidget
        return VariableDeclarationWidget(x)
    else:
        return widget_for(x)

def widget_for(x):
    # TODO: Circular import must be inside, yuck, how to fix?

    if isinstance(x, nodes.Module):
        from ModuleWidget import ModuleWidget
        return ModuleWidget(x)
    elif isinstance(x, nodes.Function):
        from FunctionWidget import FunctionWidget
        return FunctionWidget(x)
    elif isinstance(x, nodes.Variable):
        from VariableWidget import VariableWidget
        return VariableWidget(x)
    elif isinstance(x, nodes.Block):
        from BlockWidget import BlockWidget
        return BlockWidget(x)


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

    # These are only to be used as type_widget_for
    elif isinstance(x, (nodes.Ptr, nodes.Array, nodes.BuiltinType)):
        assert False

    else:
        print "Don't know how to widget %r" % (x,)
        return ccode_widget_for(x)
        #assert False, "Don't know how to widget %r" % (x,)
