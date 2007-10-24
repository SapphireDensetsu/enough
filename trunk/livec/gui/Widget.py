import pygame
from functools import partial

import gui.draw
from gui.Keymap import Keymap

class _dontchange: pass

class Widget(object):
    # frame_color is consulted first, and allowed to be None for no
    # frame.
    frame_color = None
    frame_width = 1
    bg_color = None
    selectable = True
    use_rounded_rect = True
    activated_frame_color = (40, 40, 255)
    activated_bg_color = (30, 30, 90)

    def __init__(self):
        # Use self.keymap.set_next_keymap and self.keymap for stealing
        # keys when you are above the focus.
        self.keymap = Keymap()
        self.focus_keymap = Keymap()
        self.focus_keymap.obs_activation.add_observer(self, '_keymap_')
        self.keymap.set_next_keymap(self.focus_keymap)
        
        self._prev_frame_colors = []
        
    def _keymap_activated(self):
        self.got_focus()

    def _keymap_deactivated(self):
        self.lost_focus()

    def push_frame(self, frame_color=_dontchange, bg_color=_dontchange):
        self._prev_frame_colors.append((self.frame_color, self.bg_color))
        if frame_color is not _dontchange:
            self.frame_color = frame_color
        if bg_color is not _dontchange:
            self.bg_color = bg_color

    def pop_frame(self):
        self.frame_color, self.bg_color = self._prev_frame_colors.pop()
        
    def got_focus(self):
        self.push_frame(frame_color=self.activated_frame_color,
                        bg_color=self.activated_bg_color)

    def lost_focus(self):
        self.pop_frame()
        
    def draw(self, surface, pos):
        self.draw_background(surface, pos)
        self._draw(surface, pos)
        self.draw_frame(surface, pos)

    def draw_background(self, surface, pos):
        if self.bg_color is not None:
            r = pygame.Rect(pos, self.size)
            gui.draw.rect(surface, self.bg_color, r, 0)

    def draw_frame(self, surface, pos):
        if self.frame_color is not None:
            r = pygame.Rect(pos, self.size)
            r.inflate_ip(-self.frame_width, -self.frame_width) # Half of each side
            if self.use_rounded_rect:
                dr = partial(gui.draw.rounded.rounded_rect, corner_radius=5)
            else:
                dr = gui.draw.rect
            dr(surface, self.frame_color, r, self.frame_width)

    def _draw(self, surface, pos):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()
