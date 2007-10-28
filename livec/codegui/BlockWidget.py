# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import nodes
import pygame
from gui import Keymap

from gui.Box import VBox, HBox
from gui.ProxyWidget import ProxyWidget
from gui.TextEdit import make_label
from widget_for import indented, widget_for
from InfoShower import InfoShower

from lib.observable.CacheMap import CacheMap
from lib.observable.List import List
from lib.ListProxy import ListProxy

import ccode
import style

class BlockWidget(VBox):
    default_folded = False
    kill_stmt_key = Keymap.Key(pygame.KMOD_CTRL, pygame.K_k)
    insert_statement_key = Keymap.Key(0, pygame.K_i)
    append_statement_key = Keymap.Key(0, pygame.K_o)
    
    plus_keys = (Keymap.Key(0, pygame.K_EQUALS), Keymap.Key(0, pygame.K_KP_PLUS))
    minus_keys = (Keymap.Key(0, pygame.K_MINUS), Keymap.Key(0, pygame.K_KP_MINUS))
    
    def __init__(self, block):
        self.block = block
        self.ellipsis = make_label(style.ellipsis, '...', True)
        self.proxy_widget = ProxyWidget()

        self.statement_box = VBox(CacheMap(self._widget_for,
                                           self.block.statements,
                                           with_index=True),
                                  relay_focus=True)
        self.statement_proxy = ListProxy(self.block.statements)
        self.proxy_widget.value_proxy.set(self.statement_box)

        VBox.__init__(self, List([
            make_label(style.braces, '{'),
            indented(self.proxy_widget),
            make_label(style.braces, '}'),
        ]))
        self.info_shower = InfoShower(self.ellipsis.focus_keymap.obs_activation)
        self.info_shower.info_widget = self.statement_box

        self.keymap.register_key(
            self.insert_statement_key,
            Keymap.keydown_noarg(self._insert_statement)
        )
        self.keymap.register_key(
            self.append_statement_key,
            Keymap.keydown_noarg(self._append_statement)
        )

        self.block.statements.obs_list.add_observer(self, '_statement_list_')
        self._update_delete_registration()
        self._update_fold_state()

    def _statement_list_insert(self, index, item):
        self._update_delete_registration()

    def _statement_list_pop(self, index, value):
        self._update_delete_registration()

    def _statement_list_replace(self, index, old_value, new_value):
        self._update_delete_registration()

    def _update_delete_registration(self):
        if self.block.statements:
            self.statement_box.keymap.register_key(
                self.kill_stmt_key,
                Keymap.keydown_noarg(self._delete_selected_child)
            )
        else:
            self.statement_box.keymap.unregister_key(
                self.kill_stmt_key)

    def _is_folded(self):
        return self.block.meta.get('folded', self.default_folded)

    def _update_fold_state(self):
        if self._is_folded():
            for key in self.plus_keys:
                self.keymap.register_key(key, Keymap.keydown_noarg(self._unfold))
            for key in self.minus_keys:
                self.keymap.unregister_key(key)
            widget = self.ellipsis
        else:
            for key in self.minus_keys:
                self.keymap.register_key(key, Keymap.keydown_noarg(self._fold))
            for key in self.plus_keys:
                self.keymap.unregister_key(key)
            widget = self.statement_box
        self.proxy_widget.value_proxy.set(widget)

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
        if self.statement_box.index is None or not self.block.statements:
            return
        self.block.statements.pop(self.statement_box.index)

    def _widget_for(self, (index, x)):
        if isinstance(x, nodes.Missing):
            from StatementFillerWidget import StatementFillerWidget
            return StatementFillerWidget(self.statement_proxy.proxy(index))
        w = widget_for(x)
        if ccode.is_expr(x):
            return HBox(List([
                w,
                make_label(style.semicolon, ';')
            ]), relay_focus=True)
        return w

    def _statement_index(self):
        index = self.statement_box.index
        if index is None:
            return 0
        return index

    def _insert_statement(self):
        """New statement before cursor"""
        index = self._statement_index()
        self.block.statements.insert(index, nodes.Missing())
        self.statement_box.set_index(index)

    def _append_statement(self):
        """New statement after cursor"""
        index = self._statement_index()+1
        self.block.statements.insert(index, nodes.Missing())
        self.statement_box.set_index(index)
