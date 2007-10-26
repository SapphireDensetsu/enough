# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

'''
Box widget - contains sub-widgets arranged in a row (HBox) or a column (VBox).

It has two keymaps - one for being directly in focus, and one for when
a child is in focus.

The parenting keymap is for the active child - it`s next keymap is the
child`s.  The box widget can have an active child, which is not
neccesarily the widget in focus - if the focus is not on the box, the
active child will still be remembered but it will not be in
focus. That child`s keymap will remain chained on the parenting
keymap, even if the box itself is not in focus.

'''

import pygame
from gui.Widget import Widget
from gui.Keymap import Keymap, Key
from gui.Spacer import Spacer

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
    go_down_key = Key(pygame.KMOD_SHIFT, pygame.K_RIGHT)
    go_up_key = Key(pygame.KMOD_SHIFT, pygame.K_LEFT)
    
    def __init__(self, child_list, relay_focus=False):
        Widget.__init__(self, bridge_keymap=True)
        self.child_list = child_list
        self.child_list.obs_list.add_observer(self, '_child_')

        self.relay_focus = relay_focus
        
        r = self.focus_keymap.register_key_noarg
        if not self.relay_focus:
            r(self.go_down_key, self._enter_child)

        # parenting_keymap is the keymap that's active when one of the
        # children is in focus (not the Box itself). IT's next keymap is the active child's keymap.
        self.parenting_keymap = Keymap()

        csr = self.parenting_keymap.register_key_noarg
        if not self.relay_focus:
            csr(self.go_up_key, self._leave_child)

        self.set_index(0, 1)

        if self.relay_focus or self.start_in_child:
            self._enter_child()
        else:
            self._leave_child()

    def _start_relay_focus(self):
        if self.relay_focus:
            return
        self.focus_keymap.unregister_key(self.go_down_key)
        self.parenting_keymap.unregister_key(self.go_up_key)
        self._enter_child()

    def _stop_relay_focus(self):
        if self.relay_focus:
            return
        self.focus_keymap.register_key_noarg(self.go_down_key, self._enter_child)
        self.parenting_keymap.register_key_noarg(self.go_up_key, self._leave_child)

    def _child_insert(self, index, widget):
        if index <= self.index:
            self.set_index(self.index+1, 1)
        else:
            self.set_index(self.index, 1)

    def _child_pop(self, index, value):
        if self.index is None:
            return
        if index == self.index:
            self.set_index(self.index, 1)
        elif index < self.index:
            self.set_index(self.index-1, 1)
        else:
            self.set_index(self.index)

    def _set_next_keymap(self):
        self.keymap.set_next_keymap(self.parenting_keymap)
        if self.index is not None:
            self.parenting_keymap.set_next_keymap(self.selected_child().keymap)
        else:
            self.parenting_keymap.set_next_keymap(self.focus_keymap)

    def selected_child(self):
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
        self._set_next_keymap()
        self._start_relay_focus()

    def _set_nonempty_state(self):
        self._set_next_keymap()
        self._stop_relay_focus()

    def set_index(self, new_value, scan_dir=None):
        if not self.child_list:
            self._set_empty_state()
            return
        if new_value is None:
            new_value = 0
        new_value %= len(self.child_list)
        orig_value = new_value

        assert scan_dir is not None or self.child_list[new_value].selectable, \
               "set_index used on unselectable child"
            
        while not self.child_list[new_value].selectable:
            new_value += scan_dir
            new_value %= len(self.child_list)
            if new_value == orig_value:
                self._set_empty_state()
                return
        self.index = new_value
        csu = self.parenting_keymap.unregister_key
        csr = self.parenting_keymap.register_key_noarg
        for c in self.child_list[self.index+1:]:
            if c.selectable:
                csr(self.next_key, self._next)
                break
        else:
            csu(self.next_key)
        for c in self.child_list[:self.index]:
            if c.selectable:
                csr(self.prev_key, self._prev)
                break
        else:
            csu(self.prev_key)
        self._set_nonempty_state()

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
    prev_key = Key(0, pygame.K_UP)
    next_key = Key(0, pygame.K_DOWN)
    _prev = with_doc(Box._prev, """Go up""")
    _next = with_doc(Box._next, """Go down""")

class HBox(Box):
    direction = Horizontal
    prev_key = Key(0, pygame.K_LEFT)
    next_key = Key(0, pygame.K_RIGHT)
    _prev = with_doc(Box._prev, """Go left""")
    _next = with_doc(Box._next, """Go right""")
