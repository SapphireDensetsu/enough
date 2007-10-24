import pygame
import functools
import itertools
from lib.observer import Observable

def discard_eventarg(func):
    @functools.wraps(func)
    def handler(event):
        return func()
    return handler

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

class Key(object):
    def __init__(self, modifier, key):
        self.modifier = modifier
        self.key = key

    def _essence(self):
        return (self.modifier, self.key)
    def __cmp__(self, other):
        if isinstance(other, Key):
            return cmp(self._essence(), other._essence())
        else:
            return NotImplemented
    def __hash__(self):
        return hash(self._essence())

    def name(self):
        m = mod_name(self.modifier)
        k = pygame.key.name(self.key)
        if m:
            return '%s+%s' % (m, k)
        else:
            return k
    
    __repr__ = name

    @classmethod
    def from_pygame_event(cls, event):
        mod = 0
        if event.mod & pygame.KMOD_CTRL:
            mod |= pygame.KMOD_CTRL
        elif event.mod & pygame.KMOD_ALT:
            mod |= pygame.KMOD_ALT
        elif event.mod & pygame.KMOD_SHIFT:
            mod |= pygame.KMOD_SHIFT
        return cls(mod, event.key)

class Group(object):
    def __init__(self, name, allowed_modifiers, keys):
        self.allowed_modifiers = set(allowed_modifiers)
        self.keys = set(self._flatten(key) for key in keys)
        self._name = name
    def _flatten(self, key):
        if isinstance(key, Group):
            return key.keys
        return key
    def name(self):
        return self._name
    def overlaps(self, key):
        if isinstance(key, Group):
            return bool(self.keys & key.keys) and bool(self.allowed_modifiers &
                                                       key.allowed_modifiers)
        elif isinstance(key, Key):
            return key in self
        else:
            return NotImplemented
    def __contains__(self, key):
        return key.key in self.keys and key.modifier in self.allowed_modifiers

# TODO: Its bad to assume anything about K_* here...
import string
alphanumeric = Group('Alphanumeric', [pygame.KMOD_SHIFT, 0],
                     [ord(x) for x in string.letters+string.digits] +
                     [pygame.K_UNDERSCORE, pygame.K_MINUS])

all_printable = Group('Printable symbols', [pygame.KMOD_SHIFT, 0],
                      [ord(x) for x in string.printable])

digits = Group('Digit', [0], [ord(x) for x in string.digits])

class Keymap(object):
    def __init__(self):
        self.obs_activation = Observable()
        self.obs_dict = Observable()
        self.next_keymap = None
        self.keydown_registrations = {}
        self.group_registrations = {}
        self.disabled_group_registrations = {}
        self.is_active = False

    def __contains__(self, key):
        if self.next_keymap is not None and key in self.next_keymap:
            return True
        if key in self.keydown_registrations:
            return True
        if key in self.group_registrations:
            return True
        return False

    def iterkeys(self):
        for key, value in self.iteritems():
            yield key
    
    def iteritems(self):
        if self.next_keymap is not None:
            for key, value in self.next_keymap.iteritems():
                yield key, value
        for group, value in self.group_registrations.iteritems():
            yield group, value
        for key, value in self.keydown_registrations.iteritems():
            if self.next_keymap is None or key not in self.next_keymap:
                yield key, value

    __iter__ = iterkeys

    def __getitem__(self, key):
        if self.next_keymap is not None and key in self.next_keymap:
            return self.next_keymap[key]
        if key in self.keydown_registrations:
            return self.keydown_registrations[key]
        if key in self.group_registrations:
            return self.group_registrations[key]
        raise KeyError("Unknown key", key)

    def set_next_keymap(self, keymap):
        if self.next_keymap is not None:
            if self.is_active:
                self.next_keymap.deactivate()

            for key, value in self.next_keymap.iteritems():
                if keymap is not None and isinstance(key, Key) and key in keymap:
                    # The key will remain overrided
                    continue
                self._next_keymap_remove_item(key, value)
            
            self.next_keymap.obs_dict.remove_observer(self)

        prev_keymap = self.next_keymap
        self.next_keymap = keymap
        if self.next_keymap is not None:
            self.next_keymap.obs_dict.add_observer(self, '_next_keymap_')
            for key, value in self.next_keymap.iteritems():
                if prev_keymap is not None and isinstance(key, Key) and key in prev_keymap:
                    # The key was overridden and remains so, but with a new value
                    self._next_keymap_set_item(key, prev_keymap[key], value)
                else:
                    self._next_keymap_add_item(key, value)
            if self.is_active:
                self.next_keymap.activate()

    def _shadow_groups(self, key):
        for group in self.group_registrations.keys():
            if not group.overlaps(key):
                continue
            assert group not in self.disabled_group_registrations
            gvalue = self.group_registrations.pop(group)
            self.disabled_group_registrations[group] = gvalue
            self.obs_dict.notify.remove_item(group, gvalue)

    def _unshadow_groups(self, key):
        for group in self.disabled_group_registrations.keys():
            if not group.overlaps(key):
                continue
            assert group not in self.group_registrations
            gvalue = self.disabled_group_registrations.pop(group)
            self.group_registrations[group] = gvalue
            self.obs_dict.notify.add_item(group, gvalue)

    def _next_keymap_add_item(self, key, func):
        self._shadow_groups(key)
        if key in self.keydown_registrations:
            self.obs_dict.notify.set_item(key, self.keydown_registrations[key], func)
        else:
            self.obs_dict.notify.add_item(key, func)

    def _next_keymap_remove_item(self, key, func):
        if key in self.keydown_registrations:
            self.obs_dict.notify.set_item(key, func, self.keydown_registrations[key])
        else:
            self.obs_dict.notify.remove_item(key, func)
        self._unshadow_groups(key)

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

    def register_keydown(self, key, func):
        assert isinstance(key, Key)
        assert func.__doc__, "Must use documented functions (%r)" % (func,)
        for group, func in itertools.chain(self.group_registrations.iteritems(),
                                           self.disabled_group_registrations.iteritems()):
            assert key not in group
        
        self.unregister_keydown(key)
        r = self.keydown_registrations
        r[key] = func
        if self.next_keymap is not None and key in self.next_keymap:
            return
        self.obs_dict.notify.add_item(key, func)

    def register_keydown_noarg(self, key, func):
        self.register_keydown(key, discard_eventarg(func))

    def unregister_keydown(self, key):
        assert isinstance(key, Key)
        r = self.keydown_registrations
        old_func = r.pop(key, None)
        if old_func is not None:
            if self.next_keymap is not None and key in self.next_keymap:
                return
            self.obs_dict.notify.remove_item(key, old_func)

    def register_group(self, group, func):
        assert func.__doc__, "Must use documented functions (%r)" % (func,)
        if self.next_keymap is not None:
            for key, func in self.next_keymap.iteritems():
                if group.overlaps(key):
                    self.disabled_group_registrations[group] = func
                    return
        self.group_registrations[group] = func

    def unregister_group(self, group):
        self.group_registrations.pop(group, None)
        self.disabled_group_registrations.pop(group, None)
            
    def keydown(self, event):
        mkey = Key.from_pygame_event(event)
        if self.next_keymap is not None and self.next_keymap.keydown(event):
            return True
        if mkey in self.keydown_registrations:
            func = self.keydown_registrations[mkey]
            func(event)
            return True
        for group, func in self.group_registrations.iteritems():
            if mkey in group:
                func(event)
                return True
        return False
