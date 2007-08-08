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

from functools import partial

class RowWidget(Widget):
    def __init__(self, entry_size, *args, **kw):
        # TODO add autosize flag
        super(RowWidget, self).__init__(*args, **kw)

        self.margin = 5
        self.entry_size = entry_size
        self.transposed = False # True means this is a column
        self.cached_size = None
        self.row_size = Point((1,1))*self.margin

    def add_widget_to_row(self, widget):
        self.layout_widget(len(self.widgets), widget)
        self.add_widget(widget)

    def layout_widget(self, index, widget):
        p_margin = Point((self.margin,self.margin))
        widget.size.final = self.entry_size.copy()
        widget.pos.final = p_margin + (self.entry_size + p_margin)*index
        if self.transposed:
            widget.pos.final.y = self.margin
        else:
            widget.pos.final.x = self.margin
        self.size.final = widget.size.final + widget.pos.final + Point((self.margin,self.margin))

    def transpose(self):
        self.transposed = not self.transposed
        for i,widget in enumerate(self.widgets):
            self.layout_widget(i,widget)


#------------------------------------------------------------------

def make_row_menu(label_values, choose_callback, width=200, row_height=50):
    
    # The choose_callback will get:
    # menu_widget, (label,value), clicked_widget, event
    # (event that triggered the callback (mouse up event normally))
    
    main = RowWidget(Point((width, row_height)))
    for label,value in label_values:
        w = RowWidget(Point((width, row_height)))
        w.text = label
        
        # So the user won't edit the label
        w.params.enabled = False
        w.trigger_lists['pre'].register_event_type('mouse up', partial(choose_callback, main, (label, value), w))
        main.add_widget_to_row(w)
        
    return main
