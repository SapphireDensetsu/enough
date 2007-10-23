import pygame
from Keymap import Keymap
import gui.draw

class Widget(object):
    # frame_color is consulted first, and allowed to be None for no
    # frame.
    frame_color = None
    frame_width = 1
    selectable = True

    def __init__(self):
        # Use self.keymap.set_next_keymap and self.keymap for stealing
        # keys when you are above the focus.
        self.keymap = Keymap()
        self.focus_keymap = Keymap()
        self.focus_keymap.obs_activation.add_observer(self, '_keymap_')
        self.keymap.set_next_keymap(self.focus_keymap)
        
        self._prev_frame_color = None
        
    def _keymap_activated(self):
        self._prev_frame_color = self.frame_color
        self.frame_color = (255, 0, 0)

    def _keymap_deactivated(self):
        self.frame_color = self._prev_frame_color
        self._prev_frame_color = None
        
    def draw(self, surface, pos):
        self._draw(surface, pos)
        self.draw_frame(surface, pos)

    def draw_frame(self, surface, pos):
        if self.frame_color is not None:
            r = pygame.Rect(pos, self.size)
            r.inflate_ip(-self.frame_width, -self.frame_width) # Half of each side
            gui.draw.rounded.rounded_rect(surface, self.frame_color, r, self.frame_width, 5)

    def _draw(self, surface, pos):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()
