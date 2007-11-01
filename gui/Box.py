# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

"""
Box widget - contains sub-widgets arranged in a row (HBox) or a column (VBox).

Box creates an extra keymap (on top of the usual 2 Widget keymaps),
called the parenting_keymap.

The parenting keymap is active when a child is active.  for the active
child - it`s next keymap is the child`s.  The box widget can have an
active child, which is not neccesarily the widget in focus - if the
focus is not on the box, the active child will still be remembered but
it will not be in focus. That child`s keymap will remain chained on
the parenting keymap, even if the box itself is not in focus.

"""

import pygame
from gui.Widget import Widget
from gui import Keymap
from gui.SpacerWidget import SpacerWidget

from lib.observable.List import List
from lib.observable.CacheMap import CacheMap

from gui.Table import Table

class HBox(Table):
    def __init__(self, child_list, relay_focus=False):
        Table.__init__(self, List([child_list]), relay_focus=relay_focus)

class VBox(Table):
    def __init__(self, child_list, relay_focus=False):
        Table.__init__(self, CacheMap(self._list, child_list), relay_focus=relay_focus)

    def _list(self, elem):
        return List([elem])
