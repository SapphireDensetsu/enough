# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import nodes
import pygame

from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from gui import Keymap
from codegui.widget_for import NormalWidgetMaker
from codegui import style

from lib.observable.List import List

class WhileWidget(VBox):
    convert_to_if_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_w)
    def __init__(self, node_proxy):
        self.node_proxy = node_proxy
        self.node = node_proxy.get()

        cond_part = HBox(List([
            make_label(style.while_, 'while'),
            make_label(style.paren, '('),
            NormalWidgetMaker.make(self.node.expr),
            make_label(style.paren, ')'),
        ]), relay_focus=True)
        cond_part.is_centered = True

        VBox.__init__(self, List([
            cond_part,
            NormalWidgetMaker.make(self.node.block),
        ]))

        self.focus_keymap.register_key(
            self.convert_to_if_key,
            Keymap.keydown_noarg(self._convert_to_if)
        )

    def _convert_to_if(self):
        """Convert this while to an if"""
        if_node = nodes.If(expr=self.node.expr,
                           if_true=self.node.block,
                           meta=self.node.meta)
        self.node_proxy.set(if_node)
NormalWidgetMaker.register(nodes.While, WhileWidget)
