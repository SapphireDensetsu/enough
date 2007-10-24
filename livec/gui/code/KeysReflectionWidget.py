import pygame
from gui.Box import HBox, VBox
from gui.TextEdit import make_label

from lib.observable.CacheMap import CacheMap
from lib.observable.List import List
from lib.observable.SortedItems import SortedItems

import style

# TODO: Use a Table, not a vbox of hboxes
class KeysReflectionWidget(VBox):
    selectable = False
    
    def __init__(self, root):
        self.root = root
        VBox.__init__(self, CacheMap(self._widget, SortedItems(self.root)))

    def _widget(self, (key, func)):
        from gui.Spacer import Spacer
        f = func.__doc__
        return HBox(List([
            make_label(style.keydoc_name, f),
            Spacer((style.key_space_width, 0)),
            make_label(style.key_name, key.name()),
        ]))
