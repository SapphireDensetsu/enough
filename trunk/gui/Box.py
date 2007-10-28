# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

"""
Box widget - contains sub-widgets arranged in a row (HBox) or a column (VBox).

Box creates an extra keymap (on top of the usual 2 Widget keymaps),
called the parenting_keymap.

The parenting keymap is active when a child is active.  for the active
child - it`s next keymap is the child`s.  The box widget can have an
active child, which is not neccesarily the widget in focus - if the
focus is not on the box, the active child will still be remembered but
it will not be in focus. That child`s keymap will remain chained on
the parenting keymap, even if the box itself is not in focus.

"""

import pygame
from gui.Widget import Widget
from gui import Keymap
from gui.SpacerWidget import SpacerWidget

class Direction(object): pass

class Horizontal(Direction):
    axis = 0
    oaxis = 1

class Vertical(Direction):
    axis = 1
    oaxis = 0

class Box(Widget):
    outspace = 0
    padding_widget = None
    is_centered = False
    start_in_child = True
    enter_child_key = Keymap.Key(pygame.KMOD_SHIFT, pygame.K_RIGHT)
    leave_child_key = Keymap.Key(pygame.KMOD_SHIFT, pygame.K_LEFT)
    
    def __init__(self, child_list, relay_focus=False):
        Widget.__init__(self)
        self.child_list = child_list
        self.child_list.obs_list.add_observer(self, '_child_')
        for child in self.child_list:
            child.selectable.obs_value.add_observer(self, '_child_selectable_', child)

        self.relay_focus = relay_focus
        
        # parenting_keymap is the keymap that's active when one of the
        # children is in focus (not the Box itself). IT's next keymap is the active child's keymap.
        self.parenting_keymap = Keymap.Keymap()

        if not self.relay_focus:
            self._allow_leave_child()

        self.set_index(0, 1)

        if self.relay_focus or self.start_in_child:
            self._enter_child()
        else:
            self._leave_child()

    def __getstate__(self):
        d = Widget.__getstate__(self)
        del d['parenting_keymap']
        return d
    def __setstate__(self, d):
        d['parenting_keymap'] = Keymap.Keymap()
        Widget.__setstate__(self, d)
        
    def _allow_enter_child(self):
        self.focus_keymap.register_key(
            self.enter_child_key,
            Keymap.keydown_noarg(self._enter_child)
        )

    def _disallow_enter_child(self):
        self.focus_keymap.unregister_key(self.enter_child_key)

    def _allow_leave_child(self):
        self.parenting_keymap.register_key(
            self.leave_child_key,
            Keymap.keydown_noarg(self._leave_child)
        )

    def _child_selectable_changed(self, child, old_value, new_value):
        if not new_value:
            if self.selected_child() is child:
                self.set_index(self.index+1, 1)
        else:
            if self.index is None:
                self.set_index(0, 1)

    def _child_replace(self, index, old_value, new_value):
        self._child_pop(index, old_value)
        self._child_insert(index, new_value)

    def _child_insert(self, index, child):
        child.selectable.obs_value.add_observer(self, '_child_selectable_', child)
        if index <= self.index:
            self.set_index(self.index+1, 1)
        else:
            self.set_index(self.index, 1)

    def _child_pop(self, index, child):
        child.selectable.obs_value.remove_observer(self)
        if self.index is None:
            return
        if index == self.index:
            self.set_index(self.index, 1)
        elif index < self.index:
            self.set_index(self.index-1, 1)
        else:
            self.set_index(self.index)

    def _set_next_keymap(self):
        if self.index is not None:
            self.keymap.set_next_keymap(self.parenting_keymap)
            self.parenting_keymap.set_next_keymap(self.selected_child().keymap)
        else:
            self.parenting_keymap.set_next_keymap(None)

    def selected_child(self):
        if self.index is None:
            return None
        return self.child_list[self.index]

    def _enter_child(self):
        """Go in"""
        self._set_next_keymap()

    def _leave_child(self):
        """Go out"""
        self.keymap.set_next_keymap(self.focus_keymap)

    def _next(self):
        self.set_index(self.index+1, 1)

    def _prev(self):
        self.set_index(self.index-1, -1)

    def _set_empty_state(self):
        self.index = None
        self._disallow_enter_child()
        if self.relay_focus:
            self.selectable.set(False)
        else:
            self._leave_child()

    def _set_nonempty_state(self):
        if self.relay_focus:
            self.selectable.set(True)
        else:
            self._allow_enter_child()

    def set_index(self, new_value, scan_dir=None):
        # TODO: Split this function
        if not self.child_list:
            self._set_empty_state()
            return
        if new_value is None:
            new_value = 0
        new_value %= len(self.child_list)
        orig_value = new_value

        assert scan_dir is not None or self.child_list[new_value].selectable.get(), \
               "set_index used on unselectable child"
            
        while not self.child_list[new_value].selectable.get():
            new_value += scan_dir
            new_value %= len(self.child_list)
            if new_value == orig_value:
                self._set_empty_state()
                return

        self.index = new_value

        self._update_next_prev_keys()
        self._set_nonempty_state()
        self._set_next_keymap()

    def _update_next_prev_keys(self):
        for selectability, key, func in [
            (self._next_selectable, self.next_key, self._next),
            (self._prev_selectable, self.prev_key, self._prev),
        ]:
            if selectability():
                self.parenting_keymap.register_key(key, Keymap.keydown_noarg(func))
            else:
                self.parenting_keymap.unregister_key(key)

    def _have_selectable(self, child_list):
        for child in child_list:
            if child.selectable.get():
                return True
        return False

    def _next_selectable(self):
        return self._have_selectable(self.child_list[self.index+1:])

    def _prev_selectable(self):
        return self._have_selectable(self.child_list[:self.index])

    def update(self):
        for child in self.child_list:
            child.update()
        if self.padding_widget is not None:
            self.padding_widget.update()
        def ignore_child(child, child_pos, child_size):
            pass
        self.size = self._do(ignore_child)

    def _draw(self, surface, pos):
        self_size = self.size
        def draw_child(child, child_pos, child_size):
            abs_pos = [a+b for a,b in zip(pos, child_pos)]
            if self.is_centered:
                offset = (self_size[self.direction.oaxis] -
                          child_size[self.direction.oaxis]) / 2
            else:
                offset = self.outspace
            abs_pos[self.direction.oaxis] += offset
            child.draw(surface, abs_pos)
                
        total = self._do(draw_child)
        

    def _do(self, func):
        cur = [0, 0]
        max_len = 0
        cur[self.direction.axis] = self.outspace
        
        if self.padding_widget is not None:
            padding_size = self.padding_widget.size
            padding = padding_size[self.direction.axis]
            max_len = max(max_len, padding_size[self.direction.oaxis])

        for index, child in enumerate(self.child_list):
            if index > 0 and self.padding_widget is not None:
                func(self.padding_widget, cur, padding_size)
                cur[self.direction.axis] += padding
            
            size = child.size
            func(child, cur, size)
            max_len = max(max_len, size[self.direction.oaxis])
            cur[self.direction.axis] += size[self.direction.axis]
        total = [None, None]
        total[self.direction.axis] = cur[self.direction.axis]
        total[self.direction.oaxis] = max_len+self.outspace*2
        return tuple(total)

def with_doc(old_func, doc):
    from functools import wraps
    @wraps(old_func, assigned=('__module__', '__name__'))
    def new_func(*args, **kw):
        return old_func(*args, **kw)
    new_func.__doc__ = doc
    return new_func

class VBox(Box):
    direction = Vertical
    prev_key = Keymap.Key(0, pygame.K_UP)
    next_key = Keymap.Key(0, pygame.K_DOWN)
    _prev = with_doc(Box._prev, """Go up""")
    _next = with_doc(Box._next, """Go down""")

class HBox(Box):
    direction = Horizontal
    prev_key = Keymap.Key(0, pygame.K_LEFT)
    next_key = Keymap.Key(0, pygame.K_RIGHT)
    _prev = with_doc(Box._prev, """Go left""")
    _next = with_doc(Box._next, """Go right""")
