# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox
from gui.TextEdit import make_label
from gui import Keymap

from widget_for import NormalWidgetMaker
from loop import loop
import style

from lib.observable.CacheMap import CacheMap
from lib.observable.List import List

import pygame
import nodes
import builtins

class ModuleWidget(VBox):
    add_func_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_f)
    
    def __init__(self, module_proxy):
        self.module = module_proxy.get()
        self.func_box = VBox(CacheMap(NormalWidgetMaker.make, self.module.declarations),
                             relay_focus=True)
        VBox.__init__(self, List([
            make_label(style.module_name, loop.namer.get_name(self.module)),
            self.func_box,
        ]))

        self.keymap.register_key(
            self.add_func_key,
            Keymap.keydown_noarg(self._add_func)
        )

    def _add_func(self):
        """Add a new function"""
        func = nodes.Function(
            meta=nodes.Meta(name='new_func'),
            type=nodes.FunctionType(return_type=builtins.void(),
                                    parameters=List()),
            block=nodes.Block(statements=List()),
        )
        index = self.func_box.index
        if index is None:
            index = 0
        self.module.declarations.insert(index, func)
        self.func_box.set_index(index)
NormalWidgetMaker.register(nodes.Module, ModuleWidget)
