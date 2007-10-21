from gui.Box import HBox, VBox
from gui.TextEdit import TextEdit
import pygame
from functools import partial

from List import List

class MetaWidget(VBox):
    def __init__(self, meta):
        self.meta = meta
        self.meta.add_observer(self) # TODO: observing methods
        
        VBox.__init__(self, List([
            HBox(List([TextEdit(lambda : key),
                       TextEdit(lambda : ":"),
                       TextEdit(partial(self._get_value, key),
                                partial(self._set_value, key)),
            ]))
            for key, value in sorted(self.meta.iteritems())
        ]))

    def _get_value(self, key):
        return self.meta[key]

    def _set_value(self, key, value):
        self.meta[key] = value

    def draw(self, *args, **kw):
        prev_draw_rect = self.draw_rect
        try:
            if prev_draw_rect:
                if len(self.meta) <= 1:
                    self.draw_rect = False
                else:
                    self.draw_rect = True
            return VBox.draw(self, *args, **kw)
        finally:
            self.draw_rect = prev_draw_rect
