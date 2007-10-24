from gui.Box import VBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for, style
from gui.Keymap import Key
from gui.loop import loop

from lib.observable.CacheMap import CacheMap
from lib.observable.List import List

import pygame
import nodes
import builtins

class ModuleWidget(VBox):
    def __init__(self, module):
        self.module = module
        self.func_box = VBox(CacheMap(widget_for, self.module.functions), relay_focus=True)
        VBox.__init__(self, List([
            make_label(style.module_name, loop.namer.get_name(self.module)),
            self.func_box,
        ]))

        self.keymap.register_key_noarg(Key(pygame.KMOD_CTRL, pygame.K_f),
                                       self._add_func)

    def _add_func(self):
        """Add a new function"""
        func = nodes.Function(
            meta=nodes.Meta(name='new_func'),
            type=nodes.FunctionType(return_type=builtins.void,
                                    parameters=List()),
            block=nodes.Block(statements=List()),
        )
        index = self.func_box.index
        if index is None:
            index = 0
        self.module.functions.insert(index, func)
        self.func_box.set_index(index)
