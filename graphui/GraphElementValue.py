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

import pygame

from guilib import get_default

from Lib.Point import Point


class GraphElementValue(object):
    def __init__(self, name, group_name = None, start_pos=None):
        self.name = name
        self.group_name = group_name
        self.start_pos = get_default(start_pos, Point((0,0)))

    def set_widget(self, widget):
        self._widget = widget
        self.update_widget_text()
        self._widget.pos.final = self.start_pos
    def get_widget(self):
        return self._widget
    widget = property(fget=get_widget,fset=set_widget)
    
    def update_widget_text(self):
        self._widget.text = self.name

    def entered_text(self, event):
        import string
        if event.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        elif event.unicode in (string.letters + string.digits + string.hexdigits + ' \r' + string.punctuation):
            self.name += event.unicode.replace('\r', '\n')
        self.update_widget_text()

    def dot_properties(self):
        name_text = repr(str(self.name))[1:-1] # Str translates unicode to regular strings
        return {'label': '"%s"' % (name_text,),
                #'fontsize': self._widget.default_font.get_height()/4.0,
                }
