import pygame
from gui.Box import HBox, VBox
from gui.TextEdit import make_label

from observable.CacheMap import CacheMap
from observable.List import List

import style

def mod_name(x):
    mods = []
    if x & pygame.KMOD_CTRL:
        mods.append('Control')
    if x & pygame.KMOD_SHIFT:
        mods.append('Shift')
    if x & pygame.KMOD_META:
        mods.append('Winkey')
    if x & pygame.KMOD_ALT:
        mods.append('Alt')
    return ' + '.join(mods)

def key_name((modifier, key)):
    return '%s %s' % (mod_name(modifier), pygame.key.name(key))

class KeysReflectionWidget(VBox):
    def __init__(self, root):
        self.root = root
        # TODO: Use the root keymap
        VBox.__init__(self, CacheMap(self._widget, List()))

    def _widget(self, (key, func)):
        from gui.Spacer import Spacer
        return HBox(List([
            make_label(style.key_name, key_name(key)),
            Spacer((style.key_space_width, 0)),
            make_label(style.keydoc_name, func.__doc__),
        ]))
