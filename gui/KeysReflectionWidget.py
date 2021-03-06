# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import pygame
from gui.Box import HBox, VBox
from gui.TextEdit import make_label

from lib.observable.CacheMap import CacheMap
from lib.observable.List import List
from lib.observable.SortedItems import SortedItems

from Table import Table

# TODO: Use a Table, not a vbox of hboxes
class KeysReflectionWidget(Table):
    selectable = False
    
    def __init__(self, root, key_name_style, keydoc_name_style, key_space_width=30):
        self.root = root
        self.key_name_style = key_name_style
        self.keydoc_name_style = keydoc_name_style
        self.key_space_width = key_space_width
        Table.__init__(self, CacheMap(self._key_row, SortedItems(self.root)))

    def _key_row(self, (key, func)):
        from gui.SpacerWidget import SpacerWidget
        f = func.__doc__
        return List([
            make_label(self.keydoc_name_style, f),
            SpacerWidget((self.key_space_width, 0)),
            make_label(self.key_name_style, key.name()),
        ])
