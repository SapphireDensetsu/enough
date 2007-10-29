# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import nodes
import pygame

from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from gui.SpacerWidget import SpacerWidget
from gui import Keymap
from codegui.widget_for import NormalWidgetMaker
from codegui import style

from lib.observable.List import List

class ElseWidgetMaker(NormalWidgetMaker):
    _spacer = SpacerWidget((0, 0))
    @classmethod
    def _make(cls, proxy, value):
        if value is None:
            return cls._spacer
        return VBox(List([
            make_label(style.else_, 'else'),
            NormalWidgetMaker._make(proxy, value),
        ]), relay_focus=True)

class IfWidget(VBox):
    convert_to_while_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_w)
    def __init__(self, node_proxy):
        self.node_proxy = node_proxy
        self.node = node_proxy.get()

        cond_part = HBox(List([
            make_label(style.if_, 'if'),
            make_label(style.paren, '('),
            NormalWidgetMaker.make(self.node.expr),
            make_label(style.paren, ')'),
        ]), relay_focus=True)
        cond_part.is_centered = True

        VBox.__init__(self, List([
            cond_part,
            NormalWidgetMaker.make(self.node.if_true),
            ElseWidgetMaker.make(self.node.if_false),
        ]))

        self.focus_keymap.register_key(
            self.convert_to_while_key,
            Keymap.keydown_noarg(self._convert_to_while)
        )

    def _convert_to_while(self):
        """Convert this if to a while"""
        if self.node.if_false.get() is not None:
            return
        while_node = nodes.While(expr=self.node.expr,
                                 block=self.node.if_true,
                                 meta=self.node.meta)
        self.node_proxy.set(while_node)
