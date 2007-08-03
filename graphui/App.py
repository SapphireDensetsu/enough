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

import time
import pygame
import twisted.python.log

from Lib.Point import Point

from guilib import get_default, MovingValue, ParamHolder

def mouse_pos():
    return Point(pygame.mouse.get_pos())

def Event(name, **kw):
    return pygame.event.Event(pygame.USEREVENT, name=name, **kw)


def undoable_method(func):
    def new_func(self, *args, **kw):
        undoer = func(self, *args, **kw)
        if self.undoing:
            l = self.history_redo
        else:
            l = self.history
        if len(l) < self.max_undo:
            l.append((func, undoer, args, kw))
    return new_func
    

class App(object):
    multiselect_modifier = pygame.KMOD_CTRL
    
    def __init__(self, width=800, height=600, flags=0, fps=20, widgets=None):
        self.fps = fps
        from twisted.internet.task import LoopingCall
        self._lc = LoopingCall(self._iteration)

        self.widgets = get_default(widgets, [])
        self.focused_widgets = None
        self.hovered_widget = None
        self.focus_locked = False
        self.dragging = False
        self.dragging_enabled = True
        
        self.set_size(width, height, flags)
        self.params = ParamHolder(["back_color"], "AppParams")
        self.params.back_color = (0,0,0)
        
        self.init_events()
        self.record = False

        self.history = []
        self.history_redo = []
        self.undoing = False
        self.max_undo = 25

        from Lib.Font import get_font
        self._fps_font = get_font(30)
        self._count = 0
        
    def __getinitargs__(self):
        return (self.width, self.height, self.screen_flags, self.fps, self.widgets)
    #______________________________________#
    
    def set_size(self, width, height, flags=pygame.HWSURFACE | pygame.DOUBLEBUF):
        self.width = width
        self.height = height
        self.screen_flags = flags
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
        self._lc.stop()
        from twisted.internet import reactor
        reactor.stop()

    def run(self):
        self._prev_iteration_time = time.time()
        self._rendered_fps_text = None
        d = self._lc.start(1./self.fps)
        d.addErrback(twisted.python.log.err)
        from twisted.internet import reactor
        reactor.run()

    def _iteration(self):
        cur_time = time.time()
        timedelta = (cur_time - self._prev_iteration_time)
        if timedelta == 0:
            self._cur_fps = None
        else:
            self._cur_fps = 1 / timedelta
        self._prev_iteration_time = cur_time
        self.handle_events()
        self._paint(None)

    def _draw_fps(self):
        if self._cur_fps is None:
            return
        self._count += 1
        if (self._count % 4 == 0 or self._rendered_fps_text is None):
            self._rendered_fps_text = self._fps_font.render('FPS: ' + str(int(self._cur_fps)), True, (255, 0, 0))
        # TODO: Only render text in some of the iterations...
        fps = self._rendered_fps_text
        self.screen.blit(fps, (self.screen.get_width() - fps.get_width(),
                               self.screen.get_height() - fps.get_height()))

    def handle_events(self):
        for event in pygame.event.get():
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
    def _z_ordered_widgets(self):
        return sorted((w.painting_z_order, w) for w in self.widgets)

    def paint_widgets(self, event):
        for z, widget in self._z_ordered_widgets():
            # Paint by the painting_z_order attribute order
            widget.paint(self.screen)
        
    def _paint(self, event):
        self.screen.fill(self.params.back_color)
        self.update_drag()
        self.paint_widgets(event)

        if self.record:
            pygame.draw.circle(self.screen, (255,100,100), (self.width-11, 11), 10, 0)

        self._draw_fps()
            
        pygame.display.update()

        if self.record:
            self.save_snapshot_image(self.record_dir + '/img%4.4d.BMP' % (self._frame_counter))
            self._frame_counter+=1

    def start_record(self):
        self._frame_counter = 0
        import os, time
        self.record_dir = '/tmp/record_%s' % (time.time())
        os.makedirs(self.record_dir)
        self.record = True
    def stop_record(self):
        self.record = False
        
    #______________________________________#

    def init_events(self):
        self.pygame_handlers = {}
        self.my_handlers = {'paint': [self._paint,]}
        for pg_type, handler in ((pygame.KEYDOWN, self._key_down),
                                 (pygame.MOUSEBUTTONDOWN, self._mouse_down),
                                 (pygame.MOUSEBUTTONUP, self._mouse_up),
                                 (pygame.MOUSEMOTION, self._mouse_motion),
                                 (pygame.USEREVENT, self._handle_my_event),
                                 ):
            self.register_pygame_event(pg_type, handler)
        
    #______________________________________#
    
    def _mouse_down(self, e):
        self.lock_focus(toggle=True)
        if not self.dragging_enabled:
            return
        self.dragging = True
        if self.focused_widgets:
            self.drag_start_positions = [mouse_pos() - w.pos.current for w in self.focused_widgets]
        
    def _mouse_up(self, e):
        self.unlock_focus()
        self.dragging = False

    def _mouse_motion(self, e):
        self.update_hover()
        self.update_drag()
        
    def _key_down(self, e):
        pass

    def update_drag(self):
        p = mouse_pos()
        if self.dragging:
            if self.focused_widgets:
                for w, d in zip(self.focused_widgets, self.drag_start_positions):
                    w.pos.final = p - d

    def lock_focus(self, toggle=False):
        self.update_focus(toggle=toggle)
        self.focus_locked = True
    def unlock_focus(self):
        self.focus_locked = False
        #self.update_focus()
        
    def update_focus(self, toggle=False):
        if self.focus_locked:
            return
        p = mouse_pos()
        for z, widget in reversed(self._z_ordered_widgets()):
            if widget.in_bounds(p) and widget.params.enabled:
                if not (pygame.key.get_mods() & self.multiselect_modifier):
                    self.unset_focus()
                self.set_focus(widget, toggle = toggle)
                return
        self.unset_focus()
        
    def update_hover(self):
        p = mouse_pos()
        for z, widget in reversed(self._z_ordered_widgets()):
            if widget.in_bounds(p) and widget.params.enabled:
                self.set_hover(widget)
                return
        self.unset_hover()
        
    def set_focus(self, widget, toggle = False):
        if self.focused_widgets is None:
            self.focused_widgets = []
        if widget in self.focused_widgets:
            if toggle:
                widget.params.in_focus = False
                self.focused_widgets.remove(widget)
        else:
            self.focused_widgets.append(widget)
            widget.params.in_focus = True

    def unset_focus(self):
        if self.focused_widgets is None:
            return
        for w in self.focused_widgets:
            w.params.in_focus = False
        self.focused_widgets = None

    def unset_hover(self):
        if self.hovered_widget:
            self.hovered_widget.params.in_hover = False
        self.hovered_widget = None
    def set_hover(self, widget):
        self.unset_hover()
        self.hovered_widget = widget
        self.hovered_widget.params.in_hover = True

    #_______________________________
    
    def undo(self):
        if not self.history:
            return
        doer, undoer, args, kw = self.history.pop()
        self.undoing = True
        undoer()
        self.undoing = False

    def redo(self):
        if not self.history_redo:
            return
        doer, undoer, args, kw = self.history_redo.pop()
        self.undoing = False
        undoer()
        
    def save(self, filename):
        import pickle
        f=open(filename, 'wb')
        pickle.dump(self.widgets,f,2)
    def load(self, filename):
        import pickle
        f=open(filename, 'rb')
        self.widgets = pickle.load(f)

    def save_snapshot_image(self, filename):
        pygame.image.save(pygame.display.get_surface(), filename)
