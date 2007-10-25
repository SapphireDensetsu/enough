# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from GraphWidget import GraphWidget
from Box import VBox, HBox
from Stack import Stack
from Spacer import Spacer
from Keymap import Key
import draw
import pygame

from Lib.observable.List import List

# TODO: Maybe call it LiveCEditorWidget ?
class BrowserWidget(VBox):
    def __init__(self, main_widget):
        self.main_stack = Stack()
        self.main_stack.push(main_widget)


        from loop import loop
        from KeysReflectionWidget import KeysReflectionWidget
        keys_reflection_widget = KeysReflectionWidget(loop.global_keymap)
        keys_reflection_widget.bg_color = (20,20,50)

        self.info_list = List([keys_reflection_widget,])
        info_box = HBox(self.info_list)
        info_box.selectable = False
        info_box.bg_color = (20,50,20)

        VBox.__init__(self, List([
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
        draw.offset.add_offset((self.offset_speed,0))
    def _offset_right(self):
        """Moves screen right"""

        draw.offset.add_offset((-self.offset_speed,0))
    def _offset_up(self):
        """Moves screen up"""
        draw.offset.add_offset((0,self.offset_speed))
    def _offset_down(self):
        """Moves screen down"""
        draw.offset.add_offset((0,-self.offset_speed))

    def add_info_widget(self, info):
        self.info_list.append(info)

    def remove_info_widget(self, info):
        self.info_list.remove(info)
