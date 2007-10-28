# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from gui.StackWidget import StackWidget
from gui.SpacerWidget import SpacerWidget
from gui import Keymap
from gui.KeysReflectionWidget import KeysReflectionWidget
import gui.draw
import default_style
from lib.observable.List import List

import pygame

class BrowserWidget(HBox):

    offset_right_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_LEFT)
    offset_left_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_RIGHT)
    offset_up_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_UP)
    offset_down_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_DOWN)

    def __init__(self, widget, style_module=default_style):
        self.main_stack = StackWidget()
        self.main_stack.push(widget)


        from codegui.loop import loop
        keys_reflection_widget = KeysReflectionWidget(loop.global_keymap,
                                                      style_module.key_name,
                                                      style_module.keydoc_name)
        keys_reflection_widget.bg_color = (20,20,50)

        self.info_list = List([keys_reflection_widget])
        info_box = VBox(self.info_list)
        info_box.selectable.set(False)
        info_box.bg_color = (20,50,20)

        HBox.__init__(self, List([
            self.main_stack,
            SpacerWidget((10, 0)),
            info_box,
        ]), relay_focus=True)

        register_key = self.keymap.register_key
        register_key(self.offset_right_key, Keymap.keydown_noarg(self._offset_right))
        register_key(self.offset_left_key, Keymap.keydown_noarg(self._offset_left))
        register_key(self.offset_up_key, Keymap.keydown_noarg(self._offset_down))
        register_key(self.offset_down_key, Keymap.keydown_noarg(self._offset_up))

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
