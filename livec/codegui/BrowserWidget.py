# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from gui.StackWidget import StackWidget
from gui.SpacerWidget import SpacerWidget
from gui import Keymap
from gui.KeysReflectionWidget import KeysReflectionWidget
import gui.draw
import style
from lib.observable.List import List

from gui.Table import Table

import pygame

class BrowserWidget(Table):

    offset_right_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_LEFT)
    offset_left_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_RIGHT)
    offset_up_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_UP)
    offset_down_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_DOWN)

    def __init__(self, widget):
        self.main_stack = StackWidget()
        self.main_stack.push(widget)


        from codegui.loop import loop
        keys_reflection_widget = KeysReflectionWidget(loop.global_keymap,
                                                      style.key_name,
                                                      style.keydoc_name)
        keys_reflection_widget.bg_color = (20,20,50)

        self.info_list = List([keys_reflection_widget])
        info_box = VBox(self.info_list)
        info_box.selectable.set(False)
        info_box.bg_color = (20,50,20)

        Table.__init__(self, List([List([
            self.main_stack,
            SpacerWidget((0, 10)),
            info_box,
        ])]), relay_focus=True)

    def add_info_widget(self, info):
        self.info_list.append(info)

    def remove_info_widget(self, info):
        self.info_list.remove(info)
