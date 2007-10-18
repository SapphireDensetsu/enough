import pygame
from Widget import Widget

class TextEdit(Widget):
    def __init__(self, get_text, set_text=None):
        self.get_text = get_text
        self.set_text = set_text
        self._font = pygame.font.Font(pygame.font.get_default_font(), 20)
    def draw(self, surface, pos):
        text_surface = self._font.render(self.get_text(), True, (255, 255, 255))
        surface.blit(text_surface, pos)
        return text_surface.get_size()
