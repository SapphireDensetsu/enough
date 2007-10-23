from gui.Box import VBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for, style
from observable.CacheMap import CacheMap
from observable.List import List

from gui.Keymap import discard_eventarg

import pygame
import nodes
import builtins

class ModuleWidget(VBox):
    def __init__(self, module):
        self.module = module
        ibox = VBox(CacheMap(widget_for, self.module.functions), relay_focus=True)
        VBox.__init__(self, List([
            make_label(style.module_name, self.module.meta['name']),
            ibox,
        ]))

        self.keymap.register_keydown((pygame.KMOD_CTRL, pygame.K_f), discard_eventarg(self._add_func))

    def _add_func(self):
        """Add a new function"""
        func = nodes.Function(
            meta=nodes.Meta(name='new func'),
            type=nodes.FunctionType(return_type=builtins.void,
                                    parameters=List()),
            block=nodes.Block(statements=List()),
        )
        self.module.functions.append(func)
