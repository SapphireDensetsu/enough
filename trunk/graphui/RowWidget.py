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
    def __init__(self, entry_size=None, *args, **kw):
        # TODO add autosize flag
        super(RowWidget, self).__init__(*args, **kw)

        self.margin = 5
        self.entry_size = entry_size
        self.transposed = False # True means this is a column

    def add_widget_to_row(self, widget):
        self.layout_widget(len(self.widgets), widget)
        self.add_widget(widget)

    def paint(self, *args,**kw):
        if not self.entry_size:
            self.relayout()
        return super(RowWidget,self).paint(*args,**kw)
        
    def layout_widget(self, index, widget):
        widget.update_moving() # If the widget needs to resize itself, let it
        p_margin = Point((self.margin,self.margin))
        if self.entry_size:
            widget.size.final = self.entry_size.copy()
            widget.pos.final = p_margin + (self.entry_size + p_margin)*index
            if self.transposed:
                widget.pos.final.y = self.margin
            else:
                widget.pos.final.x = self.margin
            self.size.final = widget.size.final + widget.pos.final + p_margin
        else:
            if self.transposed:
                size = Point((self.margin,self.size.final.y))
            else:
                size = Point((self.size.final.x,self.margin))

            widget.pos.final = size
            
            if self.transposed:
                self.size.final.x = max(self.size.final.x, widget.pos.final.x + widget.size.final.x + self.margin)
                self.size.final.y = widget.pos.final.y + widget.size.final.y + self.margin
            else:
                self.size.final.y = max(self.size.final.y, widget.pos.final.y + widget.size.final.y + self.margin)
                self.size.final.x = widget.pos.final.x + widget.size.final.x + self.margin

    def relayout(self):
        if not self.entry_size:
            self.size.final = Point((self.margin,self.margin))
        for i,widget in enumerate(self.widgets):
            self.layout_widget(i,widget)
        
    def transpose(self):
        self.transposed = not self.transposed
        self.relayout()


#------------------------------------------------------------------

def make_row_menu(widgets, choose_callback, entry_size=None):
    # The choose_callback will get:
    # menu_widget, obj, clicked_widget, event
    # (event that triggered the callback (mouse up event normally))
    main = RowWidget(entry_size)
    for w, obj in widgets:
        w.trigger_lists['pre'].register_event_type('mouse up', partial(choose_callback, main, obj, w))
        main.add_widget_to_row(w)
    return main

def make_row_label_menu(label_values, choose_callback, entry_size=None, text_size=None):
    if entry_size and text_size:
        raise ValueErrot("Only one of entry_size, text_size can be set")
    widgets = []
    for label,value in label_values:
        w = RowWidget(entry_size)
        w.text = label
        if not entry_size:
            w.params.autosize = 'by text'
            w.font_size = text_size
        widgets.append((w, (label,value)))
    return make_row_menu(widgets, choose_callback, entry_size=entry_size)
