## /* Copyright 2007, Noam Lewis, enoughmail@googlegroups.com */
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

from Lib.Point import Point
from Lib import Func
from Lib.Font import find_font, get_font, lines_size
from guilib import get_default, MovingValue, ParamHolder

class Widget(object):
    font_size = 40
    default_font = get_font(font_size)
    
    def __init__(self, text = '', pos=None):
        self.size = MovingValue(Point((20,20)), Point((20,20)))
        self.pos = MovingValue(Point((0,0)), Point((0,0)), step=0.3)
        
        self.font = None
        self.text = text
        self.rendered_text = None
        self.rendered_params = None

        self.font_size = 40

        self.init_params()

        from Ellipse import Ellipse
        self.shape = Ellipse(pygame.Rect(self.get_current_rect()))


    def init_params(self):
        self.params = ParamHolder(["visible", "enabled",
                                   "fore_color",
                                   "back_color",
                                   "text_color",
                                   "in_focus",
                                   "in_hover",
                                   "focus_back_color",
                                   "focus_text_color",
                                   "hover_back_color",
                                   "hover_text_color",
                                   "autosize",
                                   "user"], "WidgetParams")
        self.params.enabled = True
        self.params.visible = True
        self.params.fore_color = (100,100,200)
        self.params.back_color = (10,  10,15)
        self.params.text_color = (150,150,150)
        self.params.in_focus = False
        self.params.in_hover = False
        self.params.focus_back_color = (50,50,100)
        self.params.focus_text_color = (230,230,255)
        self.params.hover_back_color = (20,20,60)
        self.params.hover_text_color = (200,200,215)
        self.params.user = None
        self.params.autosize = "by size"
        
    def update_moving(self):
        self.render_text()
        self.size.update()
        self.pos.update()

    def render_text(self):
        if self.params.in_focus:
            text_color = self.params.focus_text_color
        elif self.params.in_hover:
            text_color = self.params.hover_text_color
        else:
            text_color = self.params.text_color

        params = (self.params.autosize, tuple(self.size.final), self.text, text_color)
        if self.params.autosize == "by text":
            params += (self.default_font,)
        if self.rendered_params == params:
            return
            
        lines = self.text.split('\n')
        if self.params.autosize == "by size":
            does_fit, self.font = find_font(lines, tuple(self.size.final*(3./4)))
        else:
            self.font = self.default_font
            if self.params.autosize == "by text":
                width, height = lines_size(self.font, lines)
                self.size.final.x = self.size.current.x = width
                self.size.final.y = self.size.current.y = height

        rendered_lines = [self.font.render(line, True, text_color)
                          for line in lines]
        size = (max(t.get_width() for t in rendered_lines),
                sum(t.get_height() for t in rendered_lines))
        self.rendered_text = pygame.Surface(size, pygame.SWSURFACE|pygame.SRCALPHA|pygame.SRCCOLORKEY, 32)
        self.rendered_params = params
        
        # TODO: Support centering and stuff?
        y = 0
        for rline in rendered_lines:
            self.rendered_text.blit(rline, (0, y))
            y += rline.get_height()

    def get_current_rect(self):
        return self.pos.current.x, self.pos.current.y, self.size.current.x, self.size.current.y
    
    def paint(self, surface):
        if not self.params.visible:
            return

        self.update_moving()
        if self.params.in_focus:
            back_color = self.params.focus_back_color
        elif self.params.in_hover:
            back_color = self.params.hover_back_color
        else:
            back_color = self.params.back_color

        self.paint_shape(surface, back_color)
        self.paint_text(surface)

    def get_shape(self):
        # TODO make the shape a mutable attribute of self?
        self.shape.rect = pygame.Rect(self.get_current_rect())
        return self.shape
    
    def paint_shape(self, surface, back_color):
        # TODO use self.get_shape to paint our shape?
        pygame.draw.ellipse(surface, back_color, self.get_current_rect(), 0)
        if self.size.current.x > 5 and self.size.current.y > 5:
            # otherwise we get a pygame error for using a width that's larger than the elipse radius
            pygame.draw.ellipse(surface, self.params.fore_color, self.get_current_rect(), 2)


    def paint_text(self, surface):
        lines = self.text.split('\n')
        text_size = Point(lines_size(self.font, lines))
        surface.blit(self.rendered_text, tuple(self.center_pos()-text_size*0.5))

    def in_bounds(self, pos):
        p = self.pos.current
        s = self.size.current
        if ((pos.x > p.x)
            and (pos.y > p.y)
            and (pos.x < p.x + s.x)
            and (pos.y < p.y + s.y)):
            return True
        return False
        
    def center_pos(self, current=True):
        if current:
            return self.pos.current+self.size.current*0.5
        return self.pos.final+self.size.final*0.5
        
    def change_font_size(self, add = 0, mul = 1):
        self.font_size *= mul
        self.font_size += add
        self.default_font = get_font(self.font_size)
        
