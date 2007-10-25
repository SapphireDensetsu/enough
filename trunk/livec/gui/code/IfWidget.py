import nodes
import pygame

from gui.Box import VBox, HBox
from gui.ProxyWidget import ProxyWidget
from gui.Spacer import Spacer
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for, indented
from gui.code import style

from lib.observable.List import List
from lib.observable.DictOfAttrs import DictOfAttrs
from lib.DictMap import DictMap

from itertools import chain


class IfWidget(VBox):
    def __init__(self, if_node):
        self.if_node = if_node

        d = DictMap(DictOfAttrs(self.if_node))
        cond_part = HBox(List([
            make_label(style.if_, 'if'),
            make_label(style.paren, '('),
            ProxyWidget(d.map('expr', widget_for)),
            make_label(style.paren, ')'),
        ]), relay_focus=True)
        cond_part.is_centered = True

        if_true_part = VBox(List([
            make_label(style.braces, '{'),
            indented(ProxyWidget(d.map('if_true', widget_for))),
            make_label(style.braces, '}'),
        ]), relay_focus=True)
            
        VBox.__init__(self, List([
            cond_part,
            if_true_part,
            ProxyWidget(d.map('if_false', self._widget_for_else)),
        ]))
    
    def _widget_for_else(self, x):
        if x is not None:
            return VBox(List([
                make_label(style.else_, 'else'),
                make_label(style.braces, '{'),
                indented(widget_for(x)),
                make_label(style.braces, '}'),
            ]), relay_focus=True)
        else:
            return Spacer((0, 0))
