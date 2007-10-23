import pygame
import functools
from observer import Observable
 
def discard_eventarg(func):
    @functools.wraps(func)
    def handler(event):
        return func()
    return handler
 
class Keymap(object):
    def __init__(self):
        self.activation = Observable()
        self.pre_keydown_registrations = {}
        self.next_keymap = None
        self.post_keydown_registrations = {}
        self.is_active = False

    def set_next_keymap(self, keymap):
        if self.is_active and self.next_keymap is not None:
            self.next_keymap.deactivate()
        self.next_keymap = keymap
        if self.is_active and self.next_keymap is not None:
            self.next_keymap.activate()

    def activate(self):
        self.is_active = True
        self.activation.notify.activated()
        if self.next_keymap is not None:
            self.next_keymap.activate()

    def deactivate(self):
        self.is_active = False
        if self.next_keymap is not None:
            self.next_keymap.deactivate()
        self.activation.notify.deactivated()

    def _keydown_registrations(self, pre):
        if pre:
            return self.pre_keydown_registrations
        else:
            return self.post_keydown_registrations
    def register_keydown(self, (modifiers, key), func, pre=False):
        r = self._keydown_registrations(pre)
        r[(modifiers, key)] = func
    def unregister_keydown(self, (modifiers, key), pre=False):
        r = self._keydown_registrations(pre)
        r.pop((modifiers, key), None)
    def keyup(self, event):
        assert False, "keyup not implemented yet"
    def keydown(self, event):
        mkey = self._mkey(event)
        if self._activate(self.pre_keydown_registrations, mkey, event):
            return True
        if self.next_keymap is not None and self.next_keymap.keydown(event):
            return True
        if self._activate(self.post_keydown_registrations, mkey, event):
            return True

    def _mkey(self, event):
        mod = 0
        if event.mod & pygame.KMOD_CTRL:
            mod |= pygame.KMOD_CTRL
        elif event.mod & pygame.KMOD_ALT:
            mod |= pygame.KMOD_ALT
        elif event.mod & pygame.KMOD_SHIFT:
            mod |= pygame.KMOD_SHIFT
        return (mod, event.key)

    def _activate(self, keymap, mkey, *args):
        if mkey not in keymap:
            return False
        handler = keymap[mkey]
        handler(*args)
        return True
