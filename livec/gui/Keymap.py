import pygame
import functools
from lib.observer import Observable

def discard_eventarg(func):
    @functools.wraps(func)
    def handler(event):
        return func()
    return handler

class Keymap(object):
    def __init__(self):
        self.obs_activation = Observable()
        self.obs_dict = Observable()
        self.next_keymap = None
        self.keydown_registrations = {}
        self.is_active = False

    def __contains__(self, key):
        if key in self.keydown_registrations:
            return True
        if self.next_keymap is not None and key in self.next_keymap:
            return True
        return False

    def iterkeys(self):
        for key, value in self.iteritems():
            yield key
    
    def iteritems(self):
        if self.next_keymap is None:
            return self.keydown_registrations.iteritems()

        return self._iteritems()

    __iter__ = iterkeys

    def __getitem__(self, key):
        if self.next_keymap is not None:
            return self.next_keymap[key]
        return self.keydown_registrations[key]

    def _iteritems(self):
        for key, value in list(self.keydown_registrations.iteritems()):
            if key not in self.next_keymap:
                yield key, value
        for key, value in list(self.next_keymap.iteritems()):
            yield key, value

    def set_next_keymap(self, keymap):
        if self.next_keymap is not None:
            if self.is_active:
                self.next_keymap.deactivate()
            for key, value in list(self.next_keymap.iteritems()):
                if key in self.keydown_registrations:
                    self.obs_dict.notify.set_item(
                        key, value, self.keydown_registrations[key])
                else:
                    self.obs_dict.notify.remove_item(key, value)
            self.next_keymap.obs_dict.remove_observer(self)
                
        self.next_keymap = keymap
        if self.next_keymap is not None:
            if self.is_active:
                self.next_keymap.activate()
            self.next_keymap.obs_dict.add_observer(self, '_next_keymap_')
            for key, value in list(self.next_keymap.iteritems()):
                if key in self.keydown_registrations:
                    self.obs_dict.notify.set_item(
                        key, self.keydown_registrations[key], value)
                else:
                    self.obs_dict.notify.add_item(key, value)

    def _next_keymap_add_item(self, key, func):
        if key in self.keydown_registrations:
            self.obs_dict.notify.remove_item(key, self.keydown_registrations[key])
        self.obs_dict.notify.add_item(key, func)

    def _next_keymap_remove_item(self, key, func):
        self.obs_dict.notify.remove_item(key, func)
        if key in self.keydown_registrations:
            self.obs_dict.notify.add_item(key, self.keydown_registrations[key])

    def _next_keymap_set_item(self, key, old_func, new_func):
        self.obs_dict.notify.set_item(key, old_func, new_func)

    def activate(self):
        self.is_active = True
        self.obs_activation.notify.activated()
        if self.next_keymap is not None:
            self.next_keymap.activate()

    def deactivate(self):
        self.is_active = False
        if self.next_keymap is not None:
            self.next_keymap.deactivate()
        self.obs_activation.notify.deactivated()

    def register_keydown(self, (modifiers, key), func):
        k = (modifiers, key)
        self.unregister_keydown(k)
        r = self.keydown_registrations
        r[k] = func
        if self.next_keymap is not None and k in self.next_keymap:
            return
        self.obs_dict.notify.add_item(k, func)

    def unregister_keydown(self, (modifiers, key)):
        k = (modifiers, key)
        r = self.keydown_registrations
        old_func = r.pop(k, None)
        if old_func is not None:
            if self.next_keymap is not None and k in self.next_keymap:
                return
            self.obs_dict.notify.remove_item(k, old_func)
            
    def keyup(self, event):
        assert False, "keyup not implemented yet"
    def keydown(self, event):
        mkey = self._mkey(event)
        if self.next_keymap is not None and self.next_keymap.keydown(event):
            return True
        if self._activate(self.keydown_registrations, mkey, event):
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
