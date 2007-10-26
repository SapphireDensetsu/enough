# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from gui.Stack import Stack
from gui.Spacer import Spacer
from gui.Keymap import Key
from gui.KeysReflectionWidget import KeysReflectionWidget
from widget_for import widget_for
import gui.draw
import style
from lib.observable.List import List

import pygame

class BrowserWidget(HBox):
    def __init__(self, node):
        self.main_stack = Stack()
        self.main_stack.push(widget_for(node))


        from gui.loop import loop
        keys_reflection_widget = KeysReflectionWidget(loop.global_keymap,
                                                      style.key_name,
                                                      style.keydoc_name)
        keys_reflection_widget.bg_color = (20,20,50)

        self.info_list = List([keys_reflection_widget,])
        info_box = VBox(self.info_list)
        info_box.selectable = False
        info_box.bg_color = (20,50,20)

        HBox.__init__(self, List([
            self.main_stack,
            Spacer((10, 0)),
            info_box,
        ]), relay_focus=True)

        def register_ctrl_key(x, func):
            self.keymap.register_key_noarg(Key(pygame.KMOD_CTRL, x), func)
        register_ctrl_key(pygame.K_LEFT, self._offset_right)
        register_ctrl_key(pygame.K_RIGHT, self._offset_left)
        register_ctrl_key(pygame.K_UP, self._offset_down)
        register_ctrl_key(pygame.K_DOWN, self._offset_up)

    offset_speed = 25
    def _offset_left(self):
        """Moves screen left"""
        gui.draw.offset.add_offset((self.offset_speed,0))
    def _offset_right(self):
        """Moves screen right"""
        gui.draw.offset.add_offset((-self.offset_speed,0))
    def _offset_up(self):
        """Moves screen up"""
        gui.draw.offset.add_offset((0,self.offset_speed))
    def _offset_down(self):
        """Moves screen down"""
        gui.draw.offset.add_offset((0,-self.offset_speed))

    def add_info_widget(self, info):
        self.info_list.append(info)

    def remove_info_widget(self, info):
        self.info_list.remove(info)
