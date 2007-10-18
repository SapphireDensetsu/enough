from gui.VBox import HBox, VBox
from gui.TextEdit import TextEdit
import pygame
from functools import partial

class MetaWidget(VBox):
    def __init__(self, meta):
        self.meta = meta
        VBox.__init__(self, self.get_children)
        self._hbox_cache = {}
        self._vbox_cache = {}

    def _clean_cache(self):
        for key, value in self._vbox_cache.iteritems():
            if key not in self.meta:
                self._vbox_cache.pop(key, None)
                self._hbox_cache.pop(key, None)

    def get_children(self):
        self._clean_cache()
        for key, value in sorted(self.meta.iteritems()):
            if key not in self._vbox_cache:
                self._vbox_cache[key] = HBox(partial(self._get_hbox_children, key, value))
            yield self._vbox_cache[key]

    def _get_hbox_children(self, key, value):
        if key not in self._hbox_cache:
            self._hbox_cache[key] = TextEdit(lambda : key), TextEdit(lambda : value)
        return self._hbox_cache[key]
