import pygame
from gui.Keymap import Keymap, Key, keydown_noarg
from MouseMap import MouseMap, MouseEvent
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import twisted.python.log

from gui import draw

class ExitLoop(Exception): pass

class Loop(object):
    fps = 20
    def __init__(self):
        self.global_keymap = Keymap()
        self.global_keymap.register_key(Key(pygame.KMOD_CTRL, pygame.K_q),
                                        keydown_noarg(self._quit))
        self.global_keymap.activate()
        self.mouse_map = MouseMap()
        self.lc = LoopingCall(self._iteration)
        
    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self._quit()
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            self.global_keymap.key_event(event)
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            self.mouse_map.mouse_event(MouseEvent(event))
    def _quit(self):
        """Quits the program"""
        self.lc.stop()
    def loop(self, display, widget):
        self.display = display
        self.widget = widget
        self.global_keymap.set_next_keymap(self.widget.keymap)

        d = self.lc.start(1. / self.fps)
        d.addCallback(lambda result: reactor.stop())
        d.addErrback(twisted.python.log.err)
        reactor.run()
    
    def _iteration(self):
        draw.offset.step()
        for event in pygame.event.get():
            self._handle_event(event)
        draw.fill(self.display, (0, 0, 0))
        self.widget.update()
        self.widget.draw(self.display, (0, 0))
        pygame.display.flip()

loop = Loop()
# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

