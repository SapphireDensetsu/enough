import nodes
from functools import partial
from gui.code import style

from gui.Box import HBox
from gui.TextEdit import make_label
from observable.List import List

def ccode_widget_for(x):
    # TODO TEMP CODE
    from gui.TextEdit import TextEdit
    from ccode import CCodeGenerator
    c = CCodeGenerator()
    return TextEdit(partial(c.ccode, x))
    

def indented(widget):
    from gui.Spacer import Spacer
    b = HBox(List([Spacer((style.indent_width, 0)), widget]), relay_focus=True)
    b.is_centered = True
    b.frame_color = None
    return b

def posttype_widget_for(x, variable):
    if isinstance(x, nodes.BuiltinType):
        from IdentifierWidget import IdentifierWidget
        return IdentifierWidget(variable, style.identifier)
    elif isinstance(x, nodes.Ptr):
        from PtrTypeWidget import PtrTypeWidget
        return PtrTypeWidget(x, variable)
    elif isinstance(x, nodes.Array):
        from ArrayTypeWidget import ArrayTypeWidget
        return ArrayTypeWidget(x, variable)
    elif isinstance(x, nodes.FunctionType):
        from FunctionTypeWidget import FunctionTypeWidget
        return FunctionTypeWidget(x, variable)
    else:
        assert False

def find_basetype(x):
    if isinstance(x, nodes.BuiltinType):
        return x
    elif isinstance(x, nodes.Ptr):
        return find_basetype(x.pointed_type)
    elif isinstance(x, nodes.Array):
        return find_basetype(x.element_type)
    elif isinstance(x, nodes.FunctionType):
        return find_basetype(x.return_type)
    else:
        assert False, "Cannot find base type of %r" % (x,)

def type_widget_for(x, variable):
    from BaseTypeWidget import BaseTypeWidget
    basetype_widget = BaseTypeWidget(find_basetype(x))

    type_widget = HBox(List([
        basetype_widget,
        make_label(style.space, ' '),
        posttype_widget_for(x, variable),
    ]))
    type_widget.is_centered = True
    return type_widget

def declaration_widget_for(x):
    if isinstance(x, nodes.Variable):
        from VariableDeclarationWidget import VariableDeclarationWidget
        return VariableDeclarationWidget(x)
    else:
        return widget_for(x)

def c_escape_common(x):
    for ch in "\\\t\r\n":
        x = x.replace(ch, repr(ch))
    return x

def c_escape_char(x):
    return c_escape_common(x).replace("'", "\\'")

def c_escape_str(x):
    return c_escape_common(x).replace('"', '\\"')

def widget_for(x):
    if isinstance(x, nodes.Module):
        from ModuleWidget import ModuleWidget
        return ModuleWidget(x)
    elif isinstance(x, nodes.Function):
        from FunctionWidget import FunctionWidget
        return FunctionWidget(x)

    elif isinstance(x, nodes.Variable):
        from IdentifierWidget import IdentifierWidget
        return IdentifierWidget(x, style.identifier)
    elif isinstance(x, nodes.Define):
        from IdentifierWidget import IdentifierWidget
        return IdentifierWidget(x, style.define)
    elif isinstance(x, nodes.EnumValue):
        from IdentifierWidget import IdentifierWidget
        return IdentifierWidget(x, style.enum)
    elif isinstance(x, nodes.Import):
        from IdentifierWidget import IdentifierWidget
        return IdentifierWidget(x, style.import_)
    
    elif isinstance(x, nodes.Block):
        from BlockWidget import BlockWidget
        return BlockWidget(x)
    elif isinstance(x, nodes.Return):
        from ReturnWidget import ReturnWidget
        return ReturnWidget(x)


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

    elif isinstance(x, nodes.Call):
        from CallWidget import CallWidget
        return CallWidget(x)
    elif isinstance(x, nodes.ArrayDeref):
        from ArrayDerefWidget import ArrayDerefWidget
        return ArrayDerefWidget(x)

    elif isinstance(x, nodes.LiteralInt):
        from LiteralWidget import LiteralWidget
        return LiteralWidget(x, repr)
    elif isinstance(x, nodes.LiteralChar):
        from LiteralWidget import LiteralWidget
        return LiteralWidget(x, lambda value: "'%c'" % c_escape_char(value))
    elif isinstance(x, nodes.LiteralString):
        from LiteralWidget import LiteralWidget
        return LiteralWidget(x, lambda value: '"%s"' % c_escape_str(value))

    # These are only to be used as type_widget_for
    elif isinstance(x, (nodes.Ptr, nodes.Array, nodes.BuiltinType)):
        assert False

    else:
        print "Don't know how to widget %r" % (x,)
        return ccode_widget_for(x)
        #assert False, "Don't know how to widget %r" % (x,)
