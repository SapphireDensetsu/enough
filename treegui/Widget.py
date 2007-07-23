import pygame

from Lib.Point import Point
from Lib import Func 
from guilib import get_default, MovingValue, ParamHolder

class Widget(object):
    def __init__(self, text = '', pos=None):
        self.size = MovingValue(Point(0,0), Point(0,0))
        self.pos = MovingValue(Point(0,0), Point(0,0), step=0.4)
        
        self.font_size = MovingValue(1,28)
        
        self.font = None
        self.text = text
        self.rendered_text = None

        self.init_params()

    def init_params(self):
        self.params = ParamHolder(["visible",
                                   "fore_color",
                                   "back_color",
                                   "text_color",
                                   "in_focus",
                                   "focus_back_color",
                                   "focus_text_color",
                                   "autosize",
                                   "user"], "WidgetParams")
        self.params.visible = True
        self.params.fore_color = (100,100,200)
        self.params.back_color = (10,  10,15)
        self.params.text_color = (200,200,210)
        self.params.in_focus = False
        self.params.focus_back_color = (50,50,100)
        self.params.focus_text_color = (230,230,255)
        self.params.user = None
        self.params.autosize = "by size"
        
    @staticmethod
    #@Func.cached # causes "default font not found"?
    def get_font(font_size):
        return pygame.font.SysFont('serif',int(font_size))
    
    def update_moving(self):
        self.render_text()
        self.size.update()
        self.pos.update()

    def render_text(self):
        if self.params.autosize == "by size":
            new_size = self.font_size.final
            while True:
                w,h = self.get_font(new_size).size(self.text)
                if (w > self.size.final.x or h > self.size.final.y):
                    break
                new_size += 1
            while True:
                w,h = self.get_font(new_size).size(self.text)
                if (w < self.size.final.x and h < self.size.final.y):
                    break
                new_size -= 1
            self.font_size.final = new_size 
            
        self.font_size.update()
        
        prev_font = self.font
        self.font = self.get_font(self.font_size.current)
        if self.font == prev_font:
            return
        if self.params.in_focus:
            text_color = self.params.focus_text_color
        else:
            text_color = self.params.text_color
        self.rendered_text = self.font.render(self.text, True, text_color)
        
        if self.params.autosize == "by text":
            self.size.final.x,self.size.final.y  = self.font.size(self.text)
            self.size.current.x,self.size.current.y  = self.font.size(self.text)

    def get_current_rect(self):
        return self.pos.current.x, self.pos.current.y, self.size.current.x, self.size.current.y
    
    def paint(self, surface):
        if not self.params.visible:
            return

        self.update_moving()
        if self.params.in_focus:
            back_color = self.params.focus_back_color
        else:
            back_color = self.params.back_color

        pygame.draw.ellipse(surface, back_color, self.get_current_rect(), 0)
        if self.size.current.x > 5 and self.size.current.y > 5:
            # otherwise we get a pygame error for using a width that's larger than the elipse radius
            pygame.draw.ellipse(surface, self.params.fore_color, self.get_current_rect(), 2)
        text_size = Point(*self.font.size(self.text))
        surface.blit(self.rendered_text, (self.center_pos()-text_size*0.5).as_tuple())

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
        
