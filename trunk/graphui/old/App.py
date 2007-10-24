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


class AppWidget(Widget):
    
    def __init__(self, width=800, height=600, flags=0, fps=20):
        super(AppWidget, self).__init__(text='', pos=Point((0,0)), size=Point((width, height)))
        self.fps = fps
        from twisted.internet.task import LoopingCall
        self._lc = LoopingCall(self._iteration)

        self.set_size(width, height, flags)
        self.params.back_color = (0,0,0)
        
        self.last_surface = None

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
        events = []
        event_map = {pygame.KEYDOWN : 'key down',
                     pygame.KEYUP : 'key up',
                     pygame.MOUSEBUTTONDOWN : 'mouse down',
                     pygame.MOUSEBUTTONUP : 'mouse up',
                     pygame.MOUSEMOTION : 'mouse motion',
                     pygame.QUIT : 'quit',
                     }
        event_type = event_map.get(pygame_event.type, None)
        if event_type is None:
            return events
        
        e = self.new_event(event_type)
        events.append(e)
        e.pygame_event = pygame_event
        if 'mouse' in e.type:
            e.pos = Point(e.pygame_event.pos)
            e.to_focused = True
        elif 'key' in e.type:
            e.key = e.pygame_event.key # TODO translate scancodes here
            e.to_focused = True
            if 'key down' == e.type:
                enter_e = e.copy()
                enter_e.type = 'enter down'
                events.append(enter_e)
            
        return events
        
    def handle_events(self):
        events_handled = False
        for pygame_event in pygame.event.get():
            for event in self.translate_event(pygame_event):
                self.handle_event(event)
                events_handled = True

        self.cause_paint(events_handled)

    zero_point = Point((0,0))
    def cause_paint(self, events_handled):
        e = self.new_event('paint')
        e.surface = self.screen
        e.to_all = True
        e.parent_offset = self.zero_point
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
        self._draw_fps()
            
        pygame.display.flip() #update()


    #_______________________________
    
    #_______________________________
