# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import pygame
from Box import HBox, VBox
from TextEdit import make_label

from Lib.observable.CacheMap import CacheMap
from Lib.observable.List import List
from Lib.observable.SortedItems import SortedItems

import style

# TODO: Use a Table, not a vbox of hboxes
class KeysReflectionWidget(VBox):
    selectable = False
    
    def __init__(self, root):
        self.root = root
        VBox.__init__(self, CacheMap(self._widget, SortedItems(self.root)))

    def _widget(self, (key, func)):
        from Spacer import Spacer
        f = func.__doc__
        return HBox(List([
            make_label(style.keydoc_name, f),
            Spacer((10, 0)),
            make_label(style.key_name, key.name()),
        ]))
