# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import nodes
from functools import partial
from codegui import style

from gui.Box import HBox
from gui.TextEdit import TextEdit, make_label
from gui.ProxyWidget import ProxyWidget
from lib.observable.List import List
from lib.observable.FuncCall import FuncCall

import ccode

def ccode_widget_for(x):
    # TODO TEMP CODE
    c = ccode.CCodeGenerator()
    return TextEdit(style.unknown_c_code, partial(c.ccode, x))
    
def indented(widget):
    from gui.SpacerWidget import SpacerWidget
    box = HBox(List([SpacerWidget((style.indent_width, 0)), widget]), relay_focus=True)
    box.is_centered = True
    box.frame_color = None
    return box

class WidgetMaker(object):
    @classmethod
    def make(cls, *proxies):
        return ProxyWidget(FuncCall(partial(cls._make, *proxies), *proxies))

class PostTypeWidgetMaker(WidgetMaker):
    @classmethod
    def _make(cls, posttype_proxy, variable_proxy, posttype, variable):
        node_type = type(posttype)
        if issubclass(node_type, nodes.BuiltinType):
            from IdentifierWidget import IdentifierWidget
            return IdentifierWidget(variable_proxy, style.identifier)
        elif issubclass(node_type, nodes.Ptr):
            from PtrPostTypeWidget import PtrPostTypeWidget
            return PtrPostTypeWidget(posttype_proxy, variable_proxy)
        elif issubclass(node_type, nodes.Array):
            from ArrayPostTypeWidget import ArrayPostTypeWidget
            return ArrayPostTypeWidget(posttype_proxy, variable_proxy)
        elif issubclass(node_type, nodes.FunctionType):
            from FunctionPostTypeWidget import FunctionPostTypeWidget
            return FunctionPostTypeWidget(posttype_proxy, variable_proxy)
        else:
            assert False

# TODO: Should this be here?
class TypeWidgetMaker(WidgetMaker):
    @classmethod
    def _make(cls, type_proxy, variable_proxy, type_, variable):
        from IdentifierWidget import IdentifierWidget
        basetype_widget = IdentifierWidget(ccode.find_basetype(type_proxy), style.base_type)

        type_widget = HBox(List([
            basetype_widget,
            make_label(style.space, ' '),
            PostTypeWidgetMaker.make(type_proxy, variable_proxy),
        ]))
        type_widget.is_centered = True
        return type_widget

class NormalWidgetMaker(WidgetMaker):
    @classmethod
    def _make(cls, proxy, value):
        from ModuleWidget import ModuleWidget
        from FunctionWidget import FunctionWidget
        from IdentifierWidget import IdentifierWidget
        from VariableWidget import VariableWidget
        from EnumValueWidget import EnumValueWidget
        from DefineValueWidget import DefineValueWidget
        from BlockWidget import BlockWidget
        from ReturnWidget import ReturnWidget
        from IfWidget import IfWidget
        from WhileWidget import WhileWidget
        from BinaryOpWidget import EqualsWidget, NotEqualsWidget, AssignWidget, SubtractWidget
        from CallWidget import CallWidget
        from ArrayDerefWidget import ArrayDerefWidget
        from LiteralStrWidget import LiteralStrWidget
        from LiteralCharWidget import LiteralCharWidget
        from LiteralIntWidget import LiteralIntWidget

        widget_map = {
            nodes.Module: ModuleWidget,
            nodes.Function: FunctionWidget,

            nodes.Variable: VariableWidget,
            nodes.Define: DefineValueWidget,
            nodes.EnumValue: EnumValueWidget,
            nodes.Import: partial(IdentifierWidget, var_style=style.import_),

            nodes.Block: BlockWidget,
            nodes.Return: ReturnWidget,

            nodes.If: IfWidget,
            nodes.While: WhileWidget,

            nodes.Equals: EqualsWidget,
            nodes.NotEquals: NotEqualsWidget,
            nodes.Assign: AssignWidget,
            nodes.Subtract: SubtractWidget,

            nodes.Call: CallWidget,
            nodes.ArrayDeref: ArrayDerefWidget,

            nodes.LiteralInt: LiteralIntWidget,
            nodes.LiteralChar: LiteralCharWidget,
            nodes.LiteralString: LiteralStrWidget,
        }

        node_type = type(value)
        for type_, factory in widget_map.iteritems():
            if issubclass(node_type, type_):
                return factory(proxy)

        is_type = issubclass(node_type, (nodes.Ptr, nodes.Array, nodes.BuiltinType))
        assert not is_type, "Only to be used in TypeWidgetMaker"

        print "Don't know how to widget %r" % (value,)
        return ccode_widget_for(proxy)
        #assert False, "Don't know how to widget %r" % (x,)

class DeclarationWidgetMaker(NormalWidgetMaker):
    @classmethod
    def _make(cls, node_proxy, node):
        node_type = type(node)
        if issubclass(node_type, nodes.Variable):
            from VariableDeclarationWidget import VariableDeclarationWidget
            return VariableDeclarationWidget(node_proxy)
        else:
            # TODO: HUH?? When can this happen?
            return NormalWidgetMaker._make(node_proxy, node)
