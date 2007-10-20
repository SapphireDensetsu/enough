import pygame

class ExitLoop(Exception): pass

def draw():
    pass

class Loop(object):
    def _handle_event(self, event):
        pass
#         if event.type == pygame.KEYDOWN:
#             self.focus.keymap.keydown(event)
    def loop(self, display, widget):
        c = pygame.time.Clock()
        while True:
            c.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                self._handle_event(event)
            display.fill((0, 0, 0))
            widget.draw(display, (0, 0))
            pygame.display.update()

loop = Loop()
