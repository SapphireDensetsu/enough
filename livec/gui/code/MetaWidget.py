from gui.VBox import VBox
from gui.TextEdit import TextEdit
import pygame

class MetaWidget(VBox):
    def __init__(self, meta):
        self.meta = meta
        VBox.__init__(self, self.get_children)
        self._cache = {}

    def _clean_cache(self):
        for key, value in self._cache.iteritems():
            if key not in self.meta:
                del self._cache[key]

    def get_children(self):
        self._clean_cache()
        for key, value in sorted(self.meta.iteritems()):
            if key not in self._cache:
                self._cache[key] = TextEdit(lambda : key)
            yield self._cache[key]
