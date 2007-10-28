# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import nodes
import pygame

from gui.Box import VBox, HBox
from gui.ProxyWidget import ProxyWidget
from gui.SpacerWidget import SpacerWidget
from gui.TextEdit import make_label
from codegui.widget_for import widget_for
from codegui import style

from lib.observable.List import List
from lib.observable.DictOfAttrs import DictOfAttrs
from lib.DictProxy import DictProxy

from itertools import chain


class IfWidget(VBox):
    def __init__(self, if_node):
        self.if_node = if_node

        d = DictProxy(DictOfAttrs(self.if_node))
        cond_part = HBox(List([
            make_label(style.if_, 'if'),
            make_label(style.paren, '('),
            ProxyWidget(d.map('expr', widget_for)),
            make_label(style.paren, ')'),
        ]), relay_focus=True)
        cond_part.is_centered = True

        VBox.__init__(self, List([
            cond_part,
            ProxyWidget(d.map('if_true', widget_for)),
            ProxyWidget(d.map('if_false', self._widget_for_else)),
        ]))
    
    def _widget_for_else(self, x):
        if x is not None:
            return VBox(List([
                make_label(style.else_, 'else'),
                widget_for(x),
            ]), relay_focus=True)
        else:
            return SpacerWidget((0, 0))
