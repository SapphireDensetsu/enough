import pygame
from Widget import Widget

class TextEdit(Widget):
    def __init__(self, get_text, set_text=None):
        self.get_text = get_text
        self.set_text = set_text
        self._font = pygame.font.Font(pygame.font.get_default_font(), 14)

    def size(self):
        def func(line, cur_height):
            return self._font.size(line)
        return self._do(func)
    
    def draw(self, surface, pos):
        def func(line, cur_height):
            text_surface = self._font.render(line, True, (255, 255, 255))
            surface.blit(text_surface, (pos[0], pos[1]+cur_height))
            return text_surface.get_size()
        self._do(func)

    def _do(self, func):
        text = self.get_text()
        size = [0, 0]
        for line in text.split('\n'):
            twidth, theight = func(line, size[1])
            size[0] = max(size[0], twidth)
            size[1] += theight
        return size
