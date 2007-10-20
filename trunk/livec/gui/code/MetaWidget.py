from gui.Box import HBox, VBox
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
        for cache in [self._vbox_cache, self._hbox_cache]:
            for key in cache:
                if key not in self.meta:
                    cache.pop(key, None)

    def get_children(self):
        self._clean_cache()
        for key, value in sorted(self.meta.iteritems()):
            if key not in self._vbox_cache:
                self._vbox_cache[key] = HBox(partial(self._get_hbox_children, key, value))
            yield self._vbox_cache[key]

    def _get_hbox_children(self, key, value):
        if key not in self._hbox_cache:
            self._hbox_cache[key] = (TextEdit(lambda : key),
                                     TextEdit(partial(self._get_value, key),
                                              partial(self._set_value, key)))
        return self._hbox_cache[key]

    def _get_value(self, key):
        return self.meta[key]

    def _set_value(self, key, value):
        self.meta[key] = value
