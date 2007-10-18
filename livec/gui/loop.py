import pygame

class ExitLoop(Exception): pass

def draw():
    pass

def loop(display, widget):
    c = pygame.time.Clock()
    while True:
        c.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
#             try:
#                 widget.handle_event(event)
#             except ExitLoop:
#                 return
        widget.draw(display, (0, 0))
        pygame.display.update()
