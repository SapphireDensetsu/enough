## /* Copyright 2007, Eyal Lotem, Noam Lewis, enoughmail@googlegroups.com */
## /*
##     This file is part of Enough.

##     Enough is free software; you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation; either version 3 of the License, or
##     (at your option) any later version.

##     Enough is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>.
## */
from __future__ import division


from Widget import Widget

from Lib.Point import Point
from guilib import MovingValue
        
class RowWidget(Widget):
    def __init__(self, *args, **kw):
        # TODO add autosize flag
        super(RowWidget, self).__init__(*args, **kw)

        self.margin = 5
        self.transposed = False # True means this is a column
        self.cached_size = None
        self.row_size = Point((1,1))*self.margin

    def update_moving(self):
        super(RowWidget, self).update_moving()
        self.update_widgets_size()
        
    def add_widget_to_row(self, widget):
        if self.transposed:
            coord = 1
        else:
            coord = 0
                
        offset = tuple(self.row_size)[coord]

        offset += self.margin
        if self.transposed:
            widget.pos.final = Point((self.margin,offset))
            self.row_size.x = max(self.row_size.x, widget.size.final.x) + self.margin
            self.row_size.y += widget.size.final.y + self.margin
        else:
            widget.pos.final = Point((offset,self.margin))
            self.row_size.y = max(self.row_size.y, widget.size.final.y) + self.margin
            self.row_size.x += widget.size.final.x + self.margin

        self.add_widget(widget)

    def update_widgets_size(self):
        if self.cached_size == self.size.final:
            return
        self.cached_size = self.size.final.copy()

        if self.row_size.x <= self.margin or self.row_size.y <= self.margin:
            return

        # Scale the widgets so that the fill us exactly (with margin left)
        x_ratio = (self.size.final.x - 2*self.margin) / (self.row_size.x - self.margin)
        y_ratio = (self.size.final.y - 2*self.margin) / (self.row_size.y - self.margin)

        print x_ratio, y_ratio
        print self.size.final, self.row_size
        for widget in self.widgets:
            widget.size.final.x *= x_ratio
            widget.size.final.y *= y_ratio

        # Dumb code again
        #self.transpose()
        #self.transpose()
        
    def transpose(self):
        self.transposed = not self.transposed
        # Dumb code.
        self.row_size = Point((1,1))*self.margin
        widgets = self.widgets
        self.widgets = []
        for widget in widgets:
            self.add_widget_to_row(widget)
