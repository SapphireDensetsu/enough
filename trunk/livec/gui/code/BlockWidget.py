import nodes
import pygame
from gui.Keymap import Key
from lib.observable.List import List

from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
from gui.code.widget_for import widget_for, ccode_widget_for

from lib.observable.CacheMap import CacheMap

class BlockWidget(VBox):
    start_in_child = True
    def __init__(self, block):
        self.block = block
        VBox.__init__(self, CacheMap(widget_for, self.block.statements))
        
        self.keymap.register_keydown_noarg(Key(pygame.KMOD_CTRL, pygame.K_i),
                                           self._add_if)


    def _add_if(self):
        """Add a new 'if'"""
        _if = nodes.If(
            expr=nodes.Equals(a=nodes.LiteralInt(value=0),
                              b=nodes.LiteralInt(value=0)),
            if_true=nodes.Block(statements=List()),
            if_false=nodes.Block(statements=List()),
        )
        self.block.statements.append(_if)
