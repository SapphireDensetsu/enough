from gui.Box import HBox, VBox
from gui.Widget import Widget

class Table(Widget):
    def __init__(self, rows):
        Widget.__init__(self)
        self.rows = rows
        #self.rows.obs_list.add_observer(self, '_row_')

        #for row in self.rows:
        #    row.obs_list.add_observer(self, '_child_')
        #    for child in row:
        #        child.selectable.obs_value.add_observer(self, '_child_selectable_', child)


    def _child_selectable_changed(self, child, old_value, new_value):
        pass

    def _child_replace(self, index, old_value, new_value):
        self._child_pop(index, old_value)
        self._child_insert(index, new_value)

    def _child_insert(self, index, child):
        child.selectable.obs_value.add_observer(self, '_child_selectable_', child)

    def _child_pop(self, index, child):
        child.selectable.obs_value.remove_observer(self)

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

            total[0] = max(total[0], self.row_sizes[rownum])

        y = 0
        for rownum, row_size in enumerate(self.row_sizes.itervalues()):
            x = 0
            for colnum, col_size in enumerate(self.column_sizes.itervalues()):
                total[1] = max(total[1], col_size)
                
                self.cell_positions[rownum,colnum] = x,y

                x += col_size
            y += row_size

        self.size = total
    

    def _draw(self, surface, pos):
        for rownum, row in enumerate(self.rows):
            for colnum, child in enumerate(row):
                abspos = [a+b for a,b in zip(self.cell_positions[rownum,colnum], pos)]
                child.draw(surface, abspos)
            
