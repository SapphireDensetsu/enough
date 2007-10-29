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
from IdentifierWidget import IdentifierWidget

import ccode

def ccode_widget_for(proxy):
    print "Unknown widget type", proxy.get(), "using ccode"
    c = ccode.CCodeGenerator()
    return TextEdit(style.unknown_c_code, partial(c.ccode, proxy))
    
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

    @classmethod
    def register(cls, node_type, factory):
        assert node_type not in cls.registrations, \
               "%r already handled by %r" % (node_type, cls.registrations[node_type])
        cls.registrations[node_type] = factory

    @classmethod
    def _find(cls, node_type, default):
        return cls.registrations.get(node_type, default)

class PostTypeWidgetMaker(WidgetMaker):
    registrations = {}
    @classmethod
    def _make(cls, posttype_proxy, variable_proxy, posttype, variable):
        node_type = type(posttype)
        factory = cls._find(node_type, None)
        assert factory is not None, "Can't make PostType widget for %r" % (node_type,)
        return factory(posttype_proxy, variable_proxy)

def build_identifier_posttype(posttype_proxy, variable_proxy):
    return IdentifierWidget(variable_proxy, style.identifier)

class DeclarationWidgetMaker(WidgetMaker):
    registrations = {}
    @classmethod
    def _make(cls, node_proxy, node):
        node_type = type(node)
        factory = cls._find(node_type, None)
        assert factory is not None, "Can't make declaration widget for %r" % (node_type,)
        return factory(node_proxy)

class NormalWidgetMaker(WidgetMaker):
    registrations = {}
    @classmethod
    def _make(cls, proxy, value):

        node_type = type(value)
        assert PostTypeWidgetMaker._find(node_type, None) is None, "Use TypeWidgetMaker on %r" % (value,)
        factory = cls._find(node_type, ccode_widget_for)
        return factory(proxy)

# Those directly making IdentifierWidget will probably need their own
# widgets, but until then they'll be registered here
PostTypeWidgetMaker.register(nodes.BuiltinType, build_identifier_posttype)
NormalWidgetMaker.register(nodes.Import, partial(IdentifierWidget, var_style=style.import_))

class TypeWidgetMaker(WidgetMaker):
    @classmethod
    def _make(cls, type_proxy, variable_proxy, type_, variable):
        basetype_widget = IdentifierWidget(ccode.find_basetype(type_proxy), style.base_type)

        type_widget = HBox(List([
            basetype_widget,
            make_label(style.space, ' '),
            PostTypeWidgetMaker.make(type_proxy, variable_proxy),
        ]))
        type_widget.is_centered = True
        return type_widget
