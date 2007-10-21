import pygame
from Widget import Widget

class TextEdit(Widget):
    def __init__(self, get_text, set_text=None):
        self.get_text = get_text
        self.set_text = set_text
        self._font = pygame.font.Font(pygame.font.get_default_font(), 14)
    def draw(self, surface, pos):
        text = self.get_text()
        size = [0,0]
        for line in text.split('\n'):
            text_surface = self._font.render(line, True, (255, 255, 255))
            surface.blit(text_surface, (pos[0], pos[1]+size[1]))
            size[0] = max(size[0], text_surface.get_size()[0])
            size[1] += text_surface.get_size()[1]
        return size #text_surface.get_size()
