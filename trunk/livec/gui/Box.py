import pygame
from gui.Widget import Widget
from gui.Keymap import Keymap, discard_event

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
    
    def __init__(self, child_list):
        Widget.__init__(self)
        self.child_list = child_list
        self.child_list.add_observer(self)
        selectables = [c for c in self.child_list if c.selectable]
        if selectables:
            self.selected_child = selectables[0]
        else:
            self.selected_child = None

        r = self.focus_keymap.register_keydown
        r((0, pygame.K_RIGHT), discard_event(self._enter_child))

        self.child_selection_keymap = Keymap()
        
        csr = self.child_selection_keymap.register_keydown
        csr((0, pygame.K_DOWN), discard_event(self._next))
        csr((0, pygame.K_UP), discard_event(self._prev))
        csr((0, pygame.K_LEFT), discard_event(self._leave_child))

        self._leave_child()

    def _set_next_keymap(self):
        self.keymap.set_next_keymap(self.child_selection_keymap)
        print self.selected_child
        self.child_selection_keymap.set_next_keymap(self.selected_child.keymap)

    def _enter_child(self):
        if self.selected_child is None:
            return
        self._set_next_keymap()
        self.in_child = True

    def _leave_child(self):
        self.in_child = False
        self.keymap.set_next_keymap(self.focus_keymap)

    def _next(self):
        if not self.in_child:
            return
        self._move_selection(1)
        self._set_next_keymap()

    def _prev(self):
        if not self.in_child:
            return
        self._move_selection(-1)
        self._set_next_keymap()

    def _move_selection(self, delta):
        selectables = [c for c in self.child_list if c.selectable]
        index = selectables.index(self.selected_child)
        index += delta
        index %= len(selectables)
        self.selected_child = selectables[index]

    def size(self):
        def ignore_child(child, child_pos, child_size):
            pass
        return self._do(ignore_child)

    def _draw(self, surface, pos):
        self_size = self.size()
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
            padding_size = self.padding_widget.size()
            padding = padding_size[self.direction.axis]
            max_len = max(max_len, padding_size[self.direction.oaxis])
        
        for index, child in enumerate(self.child_list):
            if index > 0 and self.padding_widget is not None:
                func(self.padding_widget, cur, padding_size)
                cur[self.direction.axis] += padding
            
            size = child.size()
            func(child, cur, size)
            max_len = max(max_len, size[self.direction.oaxis])
            cur[self.direction.axis] += size[self.direction.axis]
        total = [None, None]
        total[self.direction.axis] = cur[self.direction.axis]
        total[self.direction.oaxis] = max_len+self.outspace*2
        return tuple(total)

class VBox(Box):
    direction = Vertical

class HBox(Box):
    direction = Horizontal
