from gui.Widget import Widget


import pygame
from gui.Widget import Widget
from gui import Keymap
from gui.SpacerWidget import SpacerWidget


class Table(Widget):
    outspace = 0
    padding_widget = None
    is_centered = False
    start_in_child = True
    enter_child_key = Keymap.Key(pygame.KMOD_SHIFT, pygame.K_RIGHT)
    leave_child_key = Keymap.Key(pygame.KMOD_SHIFT, pygame.K_LEFT)
    right_key = Keymap.Key(0, pygame.K_LEFT)
    left_key = Keymap.Key(0, pygame.K_RIGHT)
    up_key   = Keymap.Key(0, pygame.K_UP)
    down_key = Keymap.Key(0, pygame.K_DOWN)
    
    def __init__(self, rows, transposed=False, relay_focus=False):
        Widget.__init__(self)
        self.rows = rows
        self.transposed = transposed
        #self.rows.obs_list.add_observer(self, '_row_')
        
        for rownum, row in enumerate(self.rows):
            row.obs_list.add_observer(self, '_child_', rownum)
            for child in row:
                child.selectable.obs_value.add_observer(self, '_child_selectable_', child)

        self.relay_focus = relay_focus
        
        # parenting_keymap is the keymap that's active when one of the
        # children is in focus (not the Box itself). IT's next keymap is the active child's keymap.
        self.parenting_keymap = Keymap.Keymap()

        if not self.relay_focus:
            self._allow_leave_child()

        self.set_index([0,0], [0,1])

        if self.relay_focus or self.start_in_child:
            self._enter_child()
        else:
            self._leave_child()

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
                self.set_index([self.index[0], self.index[1]+1], [0,1])
        else:
            if self.index is None:
                self.set_index([0,0], [0,1])

    def _child_replace(self, row_num, index, old_value, new_value):
        self._child_pop(row_num, index, old_value)
        self._child_insert(row_num, index, new_value)

    def _child_insert(self, row_num, index, child):
        child.selectable.obs_value.add_observer(self, '_child_selectable_', child)
        if self.index[0] != row_num:
            return
        
        if index <= self.index[1]:
            self.set_index((self.index[0], self.index[1]+1), 1)
        else:
            self.set_index(self.index, 1)

    def _child_pop(self, row_num, index, child):
        child.selectable.obs_value.remove_observer(self)
        if self.index is None or self.index[0] != row_num:
            return
        if index == self.index[1]:
            self.set_index(self.index, 1)
        elif index < self.index:
            self.set_index(self.index[0], self.index[1]-1, 1)
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
        return self.rows[self.index[0]][self.index[1]]

    def _enter_child(self):
        """Go in"""
        self._set_next_keymap()

    def _leave_child(self):
        """Go out"""
        self.keymap.set_next_keymap(self.focus_keymap)

    def _right(self):
        """Go right"""
        self.set_index([self.index[0],self.index[1]+1], [0,1])

    def _left(self):
        '''Go left'''
        self.set_index([self.index[0],self.index[1]-1], [0,-1])

    def _up(self):
        '''Go up'''
        self.set_index([self.index[0]-1,self.index[1]], [1,0])

    def _down(self):
        '''Go down'''
        self.set_index([self.index[0]+1,self.index[1]], [-1,0])

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

    def _num_columns(self):
        columns = 0
        for row in self.rows:
            columns = max(columns, len(row))
        return columns
    
    def set_index(self, new_value, scan_dir=(0,1)):
        # TODO: Split this function
        if not self.rows:
            self._set_empty_state()
            return
        if new_value is None:
            new_value = [0,0]
        columns = self._num_columns()
        new_value[0] %= len(self.rows)
        new_value[1] %= columns
        orig_value = new_value

        assert scan_dir is not None or self.rows[new_value[0]][new_value[1]].selectable.get(), \
               "set_index used on unselectable child"
            
        while not self.rows[new_value[0]][new_value[1]].selectable.get():
            new_value[0] += scan_dir[0]
            new_value[1] += scan_dir[1]
            new_value[0] %= len(self.rows)
            new_value[1] %= columns
            if new_value == orig_value:
                self._set_empty_state()
                return

        self.index = new_value

        self._update_next_prev_keys()
        self._set_nonempty_state()
        self._set_next_keymap()

    def _update_next_prev_keys(self):
        for selectability, key, func in [
            (self._right_selectable, self.right_key, self._right),
            (self._left_selectable, self.left_key, self._left),
            (self._up_selectable, self.up_key, self._up),
            (self._down_selectable, self.down_key, self._down),
        ]:
            if selectability():
                self.parenting_keymap.register_key(key, Keymap.keydown_noarg(func))
            else:
                self.parenting_keymap.unregister_key(key)

    def _row_have_selectable(self, child_list):
        for child in child_list:
            if child.selectable.get():
                return True
        return False

    def _column_have_selectable(self, start_row, column_num, direction):
        row_num = max(0, start_row + direction)
        row_num %= len(self.rows)
        
        while row_num != start_row:
            child = self.rows[row_num][column_num]
            if child.selectable.get():
                return True
            row_num = max(0,row_num + direction)
            row_num %= len(self.rows)
        
    def _right_selectable(self):
        return self._row_have_selectable(self.rows[self.index[0]][self.index[1]+1:])

    def _left_selectable(self):
        return self._row_have_selectable(self.rows[self.index[0]][:self.index[1]])

    def _up_selectable(self):
        return self._column_have_selectable(self.index[0], self.index[1], -1)
    def _down_selectable(self):
        return self._column_have_selectable(self.index[0], self.index[1], 1)


    def update(self):
        total = [0,0]
        self.column_sizes = {}
        self.row_sizes = {}
        self.cell_positions = {}
        for rownum, row in enumerate(self.rows):
            self.row_sizes.setdefault(rownum, 0)
            
            for colnum, child in enumerate(row):
                child.update()
                
                self.column_sizes.setdefault(colnum, 0)
                
                self.column_sizes[colnum] = max(self.column_sizes[colnum], child.size[0])
                self.row_sizes[rownum] = max(self.row_sizes[rownum], child.size[1])


        y = 0
        for rownum, row_size in enumerate(self.row_sizes.itervalues()):
            total[1] += row_size
            x = 0
            for colnum, col_size in enumerate(self.column_sizes.itervalues()):
                total[0] += col_size
                
                self.cell_positions[rownum,colnum] = x,y

                x += col_size
            y += row_size

        self.size = total
    

    def _draw(self, surface, pos):
        for rownum, row in enumerate(self.rows):
            for colnum, child in enumerate(row):
                    
                abspos = [a+b for a,b in zip(self.cell_positions[rownum,colnum], pos)]
                child.draw(surface, abspos)
            
