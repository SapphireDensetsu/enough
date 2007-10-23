import pygame
from Keymap import Keymap

class Widget(object):
    # frame_color is consulted first, and allowed to be None for no
    # frame.
    frame_color = None
    frame_width = 2
    selectable = True

    def __init__(self):
        # Use self.keymap.set_next_keymap and self.keymap for stealing
        # keys when you are above the focus.
        self.keymap = Keymap()
        self.focus_keymap = Keymap()
        self.focus_keymap.add_observer(self)
        self.keymap.set_next_keymap(self.focus_keymap)
        
        self._prev_frame_color = None
        
    def observe_activated(self, keymap):
        self._prev_frame_color = self.frame_color
        self.frame_color = (255, 0, 0)

    def observe_deactivated(self, keymap):
        self.frame_color = self._prev_frame_color
        self._prev_frame_color = None
        
    def draw(self, surface, pos):
        self.draw_frame(surface, pos)
        self._draw(surface, pos)

    def draw_frame(self, surface, pos):
        if self.frame_color is not None:
            r = pygame.Rect(pos, self.size)
            pygame.draw.rect(surface, self.frame_color, r, self.frame_width)

    def _draw(self, surface, pos):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()
