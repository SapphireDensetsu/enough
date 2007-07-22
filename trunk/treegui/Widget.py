import pygame

from Lib.Point import Point
from Lib import Func 
from guilib import get_default, MovingValue, ParamHolder

class Widget(object):
    def __init__(self, text = '', pos=None):
        self.size = MovingValue(Point(0,0), Point(0,0))
        self.pos = MovingValue(Point(0,0), Point(0,0), step=0.4)
        
        self.font_size = MovingValue(1,24)
        
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
                                   "user"], "WidgetParams")
        self.params.visible = True
        self.params.fore_color = (100,100,200)
        self.params.back_color = (20,  20,25)
        self.params.text_color = (210,210,255)
        self.params.in_focus = False
        self.params.focus_back_color = (50,50,100)
        self.params.user = None
        
    @staticmethod
    @Func.cached
    def get_font(font_size):
        return pygame.font.SysFont('serif',int(font_size))
    
    def update_moving(self):
        self.font_size.update()
        self.render_text()
        self.size.update()
        self.pos.update()

    def render_text(self):
        prev_font = self.font
        self.font = self.get_font(self.font_size.current)
        if self.font == prev_font:
            return
        self.rendered_text = self.font.render(self.text, True, self.params.text_color)
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
        pygame.draw.rect(surface, back_color, self.get_current_rect(), 0)
        pygame.draw.rect(surface, self.params.fore_color, self.get_current_rect(), 2)
        surface.blit(self.rendered_text, (self.pos.current.x, self.pos.current.y))

    def in_bounds(self, pos):
        p = self.pos.current
        s = self.size.current
        if ((pos.x > p.x)
            and (pos.y > p.y)
            and (pos.x < p.x + s.x)
            and (pos.y < p.y + s.y)):
            return True
        return False
        
