# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

"""
Widget does not know that it can have children. The only widget->child
relation is in subclasses (e.g Box).

Each Widget has a keymap that handles key presses events that it
receives. Now, why would a widget`s keymap receive key presses at all,
you ask? Great question!

Lets look at loop.py:
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            self.global_keymap.key_event(event)

Main loop sends events to the global keymap. Now, what does global key
map (or any other keymap) do when it gets an event like that?
"""

import pygame
from functools import partial

import gui.draw
from gui.Keymap import Keymap
from animation import MovingPos
from lib.observable.ValueContainer import ValueContainer

class _dontchange: pass

class Widget(object):
    # frame_color is consulted first, and allowed to be None for no
    # frame.
    frame_color = None
    frame_width = 1
    bg_color = None
    use_rounded_rect = True
    activated_frame_color = (40, 40, 255)
    activated_bg_color = (30, 30, 90)

    def __init__(self):
        self.focus_keymap = Keymap()
        self.focus_keymap.obs_activation.add_observer(self, '_keymap_')

        self.keymap = Keymap()
        self.keymap.set_next_keymap(self.focus_keymap)
        
        self._prev_frame_colors = []

        self._anim_pos = MovingPos()

        self.selectable = ValueContainer(True)

    def __getstate__(self):
        d = self.__dict__.copy()
        del d['keymap']
        del d['focus_keymap']
        return d
    def __setstate__(self, d):
        d['keymap'] = Keymap.Keymap()
        d['focus_keymap'] = Keymap.Keymap()
        for k,v in d.iteritems():
            self.__dict__[k] = v
            
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
        self._anim_pos.set_target(pos)
        self._anim_pos.update(0.4)
        pos = self._anim_pos.current_pos
        
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
