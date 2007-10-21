from gui.Box import HBox, VBox
from gui.TextEdit import TextEdit
import pygame
from functools import partial

class MetaWidget(VBox):
    def __init__(self, meta):
        self.meta = meta
        self.meta.add_observer(self) # TODO: observing methods
        
        VBox.__init__(self)
        for key, value in sorted(self.meta.iteritems()):
            h = HBox()
            h.add_child(TextEdit(lambda : key))
            h.add_child(TextEdit(lambda : ":"))
            h.add_child(TextEdit(partial(self._get_value, key),
                                 partial(self._set_value, key)))
            self.add_child(h)
            
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
