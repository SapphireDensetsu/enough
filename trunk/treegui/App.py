import time
import pygame

from Lib.Point import Point

from guilib import get_default, MovingValue, ParamHolder

def mouse_pos():
    x,y = pygame.mouse.get_pos()
    return Point(x,y)

def Event(name, **kw):
    return pygame.event.Event(pygame.USEREVENT, name=name, **kw)


class App(object):
    def __init__(self, width=800, height=600, flags=0):
        pygame.init()
        pygame.font.init()
        self.stop = False

        self.widgets = []
        self.focused_widget = None
        self.focus_locked = False
        self.dragging = False
        
        self.set_size(width, height, flags)
        self.params = ParamHolder(["back_color"], "AppParams")
        self.params.back_color = (0,0,0)
        
        self.init_events()

    #______________________________________#
    
    def set_size(self, width, height, flags=0):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), flags)

    def add_widget(self, widget, z = None):
        if widget in self.widgets:
            raise ValueError("Widget already exists! %r" (widget,))

        if z is None:
            self.widgets.append(widget)
        else:
            self.widgets.insert(z, widget)

    def remove_widget(self, widget):
        self.widgets.remove(widget)
        
    #______________________________________#
    
    def quit(self):
        self.stop = True

    def run(self):
        while not self.stop:
            pygame.event.pump()
            self.handle_events()

    def handle_events(self):
        events = pygame.event.get()
        self._paint(None)
        if not events:
            time.sleep(0.03)
        for event in events:
            self.handle_event(event)
        
        
    def handle_event(self, e):
        if e.type is pygame.QUIT: self.quit()
        #elif e.type is pygame.KEYDOWN and e.key == pygame.K_ESCAPE: self.quit()

        if e.type in self.pygame_handlers:
            for handler in self.pygame_handlers[e.type]:
                handler(e)
                
    def _handle_my_event(self, e):
        if e.name not in self.my_handlers:
            return
        for handler in self.my_handlers[e.name]:
            handler(e)
            
    def register_pygame_event(self, pg_type, handler):
        self.pygame_handlers.setdefault(pg_type, []).append(handler)

    def register_event(self, name, handler):
        self.my_handlers.setdefault(name, []).append(handler)

    #______________________________________#

    def _paint(self, event):
        self.screen.fill(self.params.back_color)
        for widget in self.widgets:
            widget.paint(self.screen)
        pygame.display.flip()

    #______________________________________#

    def init_events(self):
        self.pygame_handlers = {}
        self.my_handlers = {'paint': [self._paint,]}
        for pg_type, handler in ((pygame.KEYUP, self._key_up),
                                 (pygame.MOUSEBUTTONDOWN, self._mouse_down),
                                 (pygame.MOUSEBUTTONUP, self._mouse_up),
                                 (pygame.MOUSEMOTION, self._mouse_motion),
                                 (pygame.USEREVENT, self._handle_my_event),
                                 ):
            self.register_pygame_event(pg_type, handler)
        
    #______________________________________#
    
    def _mouse_down(self, e):
        self.lock_focus()
        self.dragging = True
        
    def _mouse_up(self, e):
        self.unlock_focus()
        self.dragging = False

    def _mouse_motion(self, e):
        self.update_focus()
        p = mouse_pos()
        if self.dragging:
            if self.focused_widget:
                self.focused_widget.pos.final = p
        
    def _key_up(self, e):
        self.lock_focus()


    def lock_focus(self):
        self.update_focus()
        self.focus_locked = True
    def unlock_focus(self):
        self.focus_locked = False
        self.update_focus()
        
    def update_focus(self):
        if self.focus_locked:
            return
        p = mouse_pos()
        for widget in self.widgets:
            if widget.in_bounds(p):
                self.set_focus(widget)
                return
        self.unset_focus()
        
    def set_focus(self, widget):
        self.unset_focus()
        self.focused_widget = widget
        self.focused_widget.params.in_focus = True

    def unset_focus(self):
        if self.focused_widget is None:
            return
        self.focused_widget.params.in_focus = False
        self.focused_widget = None
