import nodes
import pygame
from gui.Keymap import Key
from lib.observable.List import List

from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for, ccode_widget_for

from lib.observable.CacheMap import CacheMap
from lib.observable.List import List

import ccode
import style

class BlockWidget(VBox):
    
    default_folded = True
    
    def __init__(self, block):
        self.block = block
        self.statement_box = VBox(CacheMap(self._widget_for, self.block.statements),
                             relay_focus=True)
        self.ellipsis = make_label(style.ellipsis, '...')
        self.proxy_list = List([self.statement_box])
        VBox.__init__(self, self.proxy_list, relay_focus=True)
        
        self.statement_box.parenting_keymap.register_key_noarg(
            Key(pygame.KMOD_CTRL, pygame.K_i), self._add_if)
        
        self.statement_box.parenting_keymap.register_key_noarg(
            Key(pygame.KMOD_CTRL, pygame.K_k), self._delete_selected_child)

        self._update_fold_state()

    def _is_folded(self):
        return self.block.meta.get('folded', self.default_folded)

    def _update_fold_state(self):
        self.proxy_list.pop()
        if self._is_folded():
            self.parenting_keymap.register_key_noarg(
                Key(0, pygame.K_KP_PLUS), self._unfold)
            self.parenting_keymap.unregister_key(
                Key(0, pygame.K_KP_MINUS))
            w = self.ellipsis
        else:
            self.parenting_keymap.register_key_noarg(
                Key(0, pygame.K_KP_MINUS), self._fold)
            self.parenting_keymap.unregister_key(
                Key(0, pygame.K_KP_PLUS))
            w = self.statement_box
        self.proxy_list.append(w)

    def _fold(self):
        """Fold the code block"""
        self.block.meta['folded'] = True
        self._update_fold_state()

    def _unfold(self):
        """Unfold the code block"""
        self.block.meta['folded'] = False
        self._update_fold_state()

    def _delete_selected_child(self):
        """Delete block statement"""
        if self.index is None:
            return
        self.block.statements.pop(self.index)

    def _widget_for(self, x):
        w = widget_for(x)
        if ccode.is_expr(x):
            return HBox(List([
                w,
                make_label(style.semicolon, ';')
            ]), relay_focus=True)
        return w

    def _add_if(self):
        """Add a new 'if'"""
        _if = nodes.If(
            expr=nodes.LiteralInt(value=1),
            if_true=nodes.Block(statements=List()),
        )
        index = self.statement_box.index
        if index is None:
            index = 0
        self.block.statements.insert(index, _if)
        self.statement_box.set_index(index)
