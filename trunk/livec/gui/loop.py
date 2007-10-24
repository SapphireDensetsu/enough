import pygame
from Keymap import Keymap, Key

import gui.draw

class ExitLoop(Exception): pass

class Loop(object):
    def __init__(self):
        self.global_keymap = Keymap()
        self.global_keymap.register_keydown_noarg(Key(pygame.KMOD_CTRL, pygame.K_q),
                                                  self._quit)
        
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
            c.tick(20)
            for event in pygame.event.get():
                try:
                    self._handle_event(event)
                except ExitLoop:
                    return
            gui.draw.fill(display, (0, 0, 0))
            widget.update()
            widget.draw(display, (0, 0))
            pygame.display.flip()

loop = Loop()
