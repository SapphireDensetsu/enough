import nodes
from functools import partial
from gui.code import style

from gui.Box import HBox
from gui.TextEdit import make_label
from lib.observable.List import List

node_paths_widgets = {}
def widget_of_node_path(node_path):
    return node_paths_widgets[node_path]
    
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

c_escape_common = {
    '\\' : '\\\\',
    '\t' : '\\t',
    '\r' : '\\r',
    '\n' : '\\n',
}

c_escape_char = c_escape_common.copy()
c_escape_char["'"] = "\\'"

c_escape_str = c_escape_common.copy()
c_escape_str['"'] = '\\"'

from functools import partial, wraps

def rpartial(func, *fargs, **fkw):
    def new_func(*args, **kw):
        return partial(func, **fkw)(*(args + fargs))
    return new_func

def widget_for(x):
    from ModuleWidget import ModuleWidget
    from FunctionWidget import FunctionWidget
    from IdentifierWidget import IdentifierWidget
    from BlockWidget import BlockWidget
    from ReturnWidget import ReturnWidget
    from IfWidget import IfWidget
    from BinaryOpWidget import EqualsWidget, NotEqualsWidget, AssignWidget, SubtractWidget
    from CallWidget import CallWidget
    from ArrayDerefWidget import ArrayDerefWidget
    from LiteralWidget import LiteralWidget
    from LiteralIntWidget import LiteralIntWidget
    
    widget_map = {
        nodes.Module: ModuleWidget,
        nodes.Function: FunctionWidget,

        nodes.Variable: rpartial(IdentifierWidget, style.identifier),
        nodes.Define: rpartial(IdentifierWidget, style.define),
        nodes.EnumValue: rpartial(IdentifierWidget, style.enum),
        nodes.Import: rpartial(IdentifierWidget, style.import_),
    
        nodes.Block: BlockWidget,
        nodes.Return: ReturnWidget,


        nodes.If: IfWidget,

        nodes.Equals: EqualsWidget,
        nodes.NotEquals: NotEqualsWidget,
        nodes.Assign: AssignWidget,
        nodes.Subtract: SubtractWidget,

        nodes.Call: CallWidget,
        nodes.ArrayDeref: ArrayDerefWidget,

        nodes.LiteralInt: rpartial(LiteralIntWidget, repr),
        nodes.LiteralChar: rpartial(LiteralWidget, "'", c_escape_char),
        nodes.LiteralString: rpartial(LiteralWidget, '"', c_escape_str),
    }

    for type_,factory in widget_map.iteritems():
        if isinstance(x, type_):
            return factory(x)
        
    # These are only to be used as type_widget_for
    if isinstance(x, (nodes.Ptr, nodes.Array, nodes.BuiltinType)):
        assert False

    else:
        print "Don't know how to widget %r" % (x,)
        return ccode_widget_for(x)
        #assert False, "Don't know how to widget %r" % (x,)
