import pygame
from gui.Widget import Widget
from gui.Keymap import Keymap, Key

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
    
    def __init__(self, child_list, relay_focus=False):
        Widget.__init__(self)
        self.child_list = child_list
        self.child_list.obs_list.add_observer(self, '_child_')

        r = self.focus_keymap.register_keydown_noarg
        if not relay_focus:
            r(Key(0, pygame.K_RIGHT), self._enter_child)

        self.parenting_keymap = Keymap()

        csr = self.parenting_keymap.register_keydown_noarg
        if not relay_focus:
            csr(Key(0, pygame.K_LEFT), self._leave_child)

        selectables = [c for c in self.child_list if c.selectable]
        if selectables:
            self.selected_child = selectables[0]
            self._move_selection(0)
        else:
            self.selected_child = None

        if relay_focus or self.start_in_child:
            self._enter_child()
        else:
            self._leave_child()

    def _child_insert(self, index, widget):
        self._move_selection(0)

    def _child_pop(self, index):
        self._move_selection(0)

    def _set_next_keymap(self):
        self.keymap.set_next_keymap(self.parenting_keymap)
        self.parenting_keymap.set_next_keymap(self.selected_child.keymap)

    def _enter_child(self):
        """Go in"""
        if self.selected_child is None:
            return
        self._set_next_keymap()
        self.in_child = True

    def _leave_child(self):
        """Go out"""
        self.in_child = False
        self.keymap.set_next_keymap(self.focus_keymap)

    def _next(self):
        """Go to the next"""
        if not self.in_child:
            return
        self._move_selection(1)
        self._set_next_keymap()

    def _prev(self):
        """Go to the prev"""
        if not self.in_child:
            return
        self._move_selection(-1)
        self._set_next_keymap()

    def _move_selection(self, delta):
        selectables = [c for c in self.child_list if c.selectable]
        index = selectables.index(self.selected_child)
        index += delta
##        index %= len(selectables)
        csu = self.parenting_keymap.unregister_keydown
        csr = self.parenting_keymap.register_keydown_noarg
        if index == len(selectables)-1:
            csu(Key(0, pygame.K_DOWN))
        else:
            csr(Key(0, pygame.K_DOWN), self._next)
        if index == 0:
            csu(Key(0, pygame.K_UP))
        else:
            csr(Key(0, pygame.K_UP), self._prev)
        self.selected_child = selectables[index]

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

class VBox(Box):
    direction = Vertical

class HBox(Box):
    direction = Horizontal
