# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

"""The things a keymap does:

1. Pass given keys to 'next' keymap (considered more 'specific') which
is stronger/overrides the keymap itself.

2. If the next keymap does not know the key, then it tries to handle
   it itself according to a map it holds that maps specific (modifier,
   key) to funcs, and then, also according to a map of broader groups
   to funcs."""

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
    def __init__(self, modifier, key, event_type=pygame.KEYDOWN):
        self.modifier = modifier
        self.key = key
        assert event_type in [pygame.KEYUP, pygame.KEYDOWN]
        self.event_type = event_type

    def _essence(self):
        return (self.modifier, self.key, self.event_type)
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
            s = '%s+%s' % (m, k)
        else:
            s = k
        if self.event_type == pygame.KEYUP:
            s += ' (keyup)'
        return s
    
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
        return cls(mod, event.key, event.type)

class Group(object):
    def __init__(self, name, allowed_modifiers, keys, event_type=pygame.KEYDOWN):
        self.allowed_modifiers = set(allowed_modifiers)
        self.keys = set(self._flatten(key) for key in keys)
        self._name = name
        self.event_type = event_type
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
        return key.key in self.keys and key.modifier in self.allowed_modifiers and key.event_type == self.event_type

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

        # Cache these cause they are rather expensive to generate and
        # used a LOT.
        self.notify_remove_item = self.obs_dict.notify.remove_item
        self.notify_add_item = self.obs_dict.notify.add_item
        self.notify_replace_item = self.obs_dict.notify.replace_item
        
        self.next_keymap = None
        self.key_registrations = {}
        self.group_registrations = {}
        self.disabled_group_registrations = {}
        self.is_active = False

    def __contains__(self, key):
        if self.next_keymap is not None and key in self.next_keymap:
            return True
        if key in self.key_registrations:
            return True
        if key in self.group_registrations:
            return True
        return False

    def iterkeys(self):
        for key, value in self.iteritems():
            yield key
    
    def iteritems(self):
        overridden = set()
        if self.next_keymap is not None:
            for key, value in self.next_keymap.iteritems():
                overridden.add(key)
                yield key, value
        for group, value in self.group_registrations.iteritems():
            yield group, value
        for key, value in self.key_registrations.iteritems():
            if key not in overridden:
                yield key, value

    __iter__ = iterkeys

    def __getitem__(self, key):
        if self.next_keymap is not None and key in self.next_keymap:
            return self.next_keymap[key]
        if key in self.key_registrations:
            return self.key_registrations[key]
        if key in self.group_registrations:
            return self.group_registrations[key]
        raise KeyError("Unknown key", key)

    def set_next_keymap(self, keymap):
        if self.next_keymap is keymap:
            return
        if self.next_keymap is not None:
            if self.is_active:
                self.next_keymap.deactivate()

            # TODO: How to export to function?
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
                    self._next_keymap_replace_item(key, prev_keymap[key], value)
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
            self.notify_remove_item(group, gvalue)

    def _unshadow_groups(self, key):
        for group in self.disabled_group_registrations.keys():
            if not group.overlaps(key):
                continue
            assert group not in self.group_registrations
            gvalue = self.disabled_group_registrations.pop(group)
            self.group_registrations[group] = gvalue
            self.notify_add_item(group, gvalue)

    def _next_keymap_add_item(self, key, func):
        self._shadow_groups(key)
        if key in self.key_registrations:
            self.notify_replace_item(key, self.key_registrations[key], func)
        else:
            self.notify_add_item(key, func)

    def _next_keymap_remove_item(self, key, func):
        if key in self.key_registrations:
            self.notify_replace_item(key, func, self.key_registrations[key])
        else:
            self.notify_remove_item(key, func)
        self._unshadow_groups(key)

    def _next_keymap_replace_item(self, key, old_func, new_func):
        self.notify_replace_item(key, old_func, new_func)

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

    def register_key(self, key, func):
        assert isinstance(key, Key)
        assert func.__doc__, "Must use documented functions (%r)" % (func,)
        for group, func in itertools.chain(self.group_registrations.iteritems(),
                                           self.disabled_group_registrations.iteritems()):
            assert key not in group
        
        self.unregister_key(key)
        r = self.key_registrations
        r[key] = func
        if self.next_keymap is not None and key in self.next_keymap:
            return
        self.notify_add_item(key, func)

    def register_key_noarg(self, key, func):
        self.register_key(key, discard_eventarg(func))

    def unregister_key(self, key):
        assert isinstance(key, Key)
        r = self.key_registrations
        old_func = r.pop(key, None)
        if old_func is not None:
            if self.next_keymap is not None and key in self.next_keymap:
                return
            self.notify_remove_item(key, old_func)

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
            
    def key_event(self, event):
        mkey = Key.from_pygame_event(event)
        if self.next_keymap is not None and self.next_keymap.key_event(event):
            return True
        if mkey in self.key_registrations:
            func = self.key_registrations[mkey]
            func(event)
            return True
        for group, func in self.group_registrations.iteritems():
            if mkey in group:
                func(event)
                return True
        return False
