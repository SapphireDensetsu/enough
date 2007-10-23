import pygame
from Keymap import Keymap, discard_eventarg

import gui.draw

class ExitLoop(Exception): pass

class Loop(object):
    def __init__(self):
        self.global_keymap = Keymap()
        self.global_keymap.register_keydown((pygame.KMOD_CTRL, pygame.K_q),
                                            discard_eventarg(self._quit))
        self.global_keymap.register_keydown((pygame.KMOD_CTRL, pygame.K_LEFT),
                                            discard_eventarg(self._offset_right))
        self.global_keymap.register_keydown((pygame.KMOD_CTRL, pygame.K_RIGHT),
                                            discard_eventarg(self._offset_left))
        self.global_keymap.register_keydown((pygame.KMOD_CTRL, pygame.K_DOWN),
                                            discard_eventarg(self._offset_up))
        self.global_keymap.register_keydown((pygame.KMOD_CTRL, pygame.K_UP),
                                            discard_eventarg(self._offset_down))
        
    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self._quit()
        if event.type == pygame.KEYDOWN:
            self.global_keymap.keydown(event)
#         elif event.type == pygame.KEYUP:
#             self.global_keymap.keyup(event)
    def _quit(self):
        """Quits the program"""
        raise ExitLoop()
    def loop(self, display, widget):
        self.global_keymap.activate()
        self.global_keymap.set_next_keymap(widget.keymap)
        c = pygame.time.Clock()
        while True:
            gui.draw.offset.step()
            c.tick(30)
            for event in pygame.event.get():
                try:
                    self._handle_event(event)
                except ExitLoop:
                    return
            gui.draw.fill(display, (0, 0, 0))
            widget.update()
            widget.draw(display, (0, 0))
            pygame.display.flip()

    offset_speed = 25
    def _offset_left(self):
        """Moves screen left"""
        gui.draw.offset.add_offset((self.offset_speed,0))
    def _offset_right(self):
        """Moves screen right"""
        gui.draw.offset.add_offset((-self.offset_speed,0))
    def _offset_up(self):
        """Moves screen up"""
        gui.draw.offset.add_offset((0,self.offset_speed))
    def _offset_down(self):
        """Moves screen down"""
        gui.draw.offset.add_offset((0,-self.offset_speed))

loop = Loop()
