from gui.Box import VBox
from gui.Stack import Stack
from gui.Spacer import Spacer
from gui.Keymap import Key
from widget_for import widget_for
import gui.draw
import pygame

# TODO: Maybe call it LiveCEditorWidget ?
class BrowserWidget(VBox):
    def __init__(self, node):
        self.main_stack = Stack()
        self.main_stack.push(widget_for(node))

        self.info_stack = Stack()
        self.info_stack.push(Spacer((0, 0)))

        from gui.loop import loop
        from KeysReflectionWidget import KeysReflectionWidget
        keys_reflection_widget = KeysReflectionWidget(loop.global_keymap)

        from lib.observable.List import List
        VBox.__init__(self, List([
            self.main_stack,
            self.info_stack,
            Spacer((0, 20)),
            keys_reflection_widget,
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
        self.info_stack.push(info)

    def remove_info_widget(self, info):
        self.info_stack.remove(info)
