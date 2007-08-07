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



from Widget import Widget

from Lib.Point import Point
from guilib import MovingValue

        
class RowWidget(Widget):
    def __init__(self, *args, **kw):
        super(RowWidget, self).__init__(*args, **kw)

        self.margin = 5
        self.transposed = False # True means this is a column

    def add_widget_to_row(self, widget):
        if self.transposed:
            coord = 1
        else:
            coord = 0
                
        offset = tuple(self.size.final)[coord]

        offset += self.margin
        if self.transposed:
            widget.pos.final = Point((0,offset))
            self.size.final.x = max(self.size.final.x, widget.size.final.x)
            self.size.final.y += widget.size.final.y
        else:
            widget.pos.final = Point((offset,0))
            self.size.final.y = max(self.size.final.y, widget.size.final.y)
            self.size.final.x += widget.size.final.x

        self.add_widget(widget)

        
    def transpose(self):
        self.transposed = not self.transposed
        # Dumb code.
        self.size.final = Point((0,0))
        widgets = self.widgets
        self.widgets = []
        for widget in widgets:
            self.add_widget_to_row(widget)
