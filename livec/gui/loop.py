import pygame
from Keymap import Keymap, discard_eventarg

class ExitLoop(Exception): pass

class Loop(object):
    def __init__(self):
        self.global_keymap = Keymap()
        self.global_keymap.register_keydown((pygame.KMOD_CTRL, pygame.K_q),
                                            discard_eventarg(self._quit))
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
            c.tick(15)
            for event in pygame.event.get():
                try:
                    self._handle_event(event)
                except ExitLoop:
                    return
            display.fill((0, 0, 0))
            widget.update()
            widget.draw(display, (0, 0))
            pygame.display.update()

loop = Loop()
