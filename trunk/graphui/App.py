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
from Lib.Event import Event

from guilib import get_default, MovingValue, ParamHolder

from Widget import Widget


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
    

class AppWidget(Widget):
    
    def __init__(self, width=800, height=600, flags=0, fps=20):
        super(AppWidget, self).__init__(text='', pos=Point((0,0)), size=Point((width, height)))
        self.fps = fps
        from twisted.internet.task import LoopingCall
        self._lc = LoopingCall(self._iteration)

        self.set_size(width, height, flags)
        self.params.back_color = (0,0,0)
        
        self.record = False

        self.history = []
        self.history_redo = []
        self.undoing = False
        self.max_undo = 25

        from Lib.Font import get_font
        self._fps_font = get_font(30)
        self._count = 0
    #______________________________________#
    
    def set_size(self, width, height, flags=pygame.HWSURFACE | pygame.DOUBLEBUF):
        self.width = width
        self.height = height
        self.screen_flags = flags
        self.screen = pygame.display.set_mode((width, height), flags)

    #______________________________________#
    
    def quit(self, event):
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

    def new_event(self, event_type):
        e = Event(event_type)
        e.to_focused = False
        e.to_all = False
        return e

    def in_bounds(self, pos):
        return True
    
    def translate_event(self, pygame_event):
        event_map = {pygame.KEYDOWN : 'key down',
                     pygame.KEYUP : 'key up',
                     pygame.MOUSEBUTTONDOWN : 'mouse down',
                     pygame.MOUSEBUTTONUP : 'mouse up',
                     pygame.MOUSEMOTION : 'mouse motion',
                     pygame.QUIT : 'quit',
                     }
        event_type = event_map.get(pygame_event.type, None)
        if event_type is None:
            return None
        e = self.new_event(event_type)
        e.pygame_event = pygame_event
        if 'mouse' in e.type:
            e.pos = Point(e.pygame_event.pos)
            e.to_focused = True
        elif 'key' in e.type:
            e.key = e.pygame_event.key # TODO translate scancodes here
            e.to_focused = True
        return e
        
    def handle_events(self):
        for pygame_event in pygame.event.get():
            event = self.translate_event(pygame_event)
            if event is not None:
                self.handle_event(event)

        e = self.new_event('paint')
        e.surface = self.screen
        e.to_all = True
        self.handle_event(e)

    def _init_event_triggers(self):
        super(AppWidget, self)._init_event_triggers()
        self.trigger_lists['pre'].register_event_type('quit', self.quit, forced=True)

    #______________________________________#
    
    def paint(self, event):
        #surface = self.screen
        surface = event.surface
        surface.fill(self.params.back_color)
        
        self.paint_widgets(event)

        # This is the post-painting stuff - flip display, etc.
        if self.record:
            pygame.draw.circle(surface, (255,100,100), (self.width-11, 11), 10, 0)

        self._draw_fps()
            
        pygame.display.update()

        if self.record:
            self.save_snapshot_image(self.record_dir + '/img%4.4d.BMP' % (self._frame_counter))
            self._frame_counter+=1


    #_______________________________
    
    def start_record(self):
        self._frame_counter = 0
        import os, time
        self.record_dir = '/tmp/record_%s' % (time.time())
        os.makedirs(self.record_dir)
        self.record = True
    def stop_record(self):
        self.record = False
        
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

    def save_snapshot_image(self, filename, width=None, height=None):
        width = get_default(width, self.width)
        height = get_default(height, self.height)
        pygame.image.save(pygame.transform.scale(pygame.display.get_surface(), (width,height)), filename)

    def push_widgets(self, new_widgets=None):
        new_widgets = get_default(new_widgets, [])
        self.widgets_stack.append(self.widgets)
        self.widgets = new_widgets
    def pop_widgets(self):
        if self.widgets_stack:
            self.widgets = self.widgets_stack.pop()
        
