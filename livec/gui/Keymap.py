import pygame

class Keymap(object):
    def __init__(self):
        self.pre_keydown_registrations = {}
        self.next_keymap = None
        self.post_keydown_registrations = {}
    def set_next_keymap(self, keymap):
        self.next_keymap = keymap
    def _keydown_registrations(self, pre):
        if pre:
            return self.pre_keydown_registrations
        else:
            return self.post_keydown_registrations
    def register_keydown(self, (modifiers, key), func, pre=False):
        r = self._keydown_registrations(pre)
        assert (modifiers, key) not in r
        r[(modifiers, key)] = func
    def unregister_keydown(self, (modifiers, key)):
        del r[(modifiers, key)]
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
        return handler(*args)
