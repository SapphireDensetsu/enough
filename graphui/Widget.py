'''
Widget does not know that it can have children. The only widget->child
relation is in Box.

Each Widget has a keymap that handles key presses events that it
receives. Now, why would a widget`s keymap receive key presses at all,
you ask? Great question!

Lets look at loop.py:
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            self.global_keymap.key_event(event)

Main loop sends events to the global keymap. Now, what does global key
map (or any other keymap) do when it gets an event like that?

The things it tries to do are:

1. Pass it to its "next keymap" the "next" keymap (of a child, thus
more "specific" widget) is stronger/overrides the keymap itself.

2. If the next keymap does not know the key, then it tries to handle
it itself according to a map it holds that maps specific
(modifier,key) to funcs, and then, also according to a map of broader
groups to funcs (it checks group after group if thee key is in it and
uses the func).

 '''
import pygame
from functools import partial

import gui.draw
from gui.Keymap import Keymap
from guilib import MovingValue
from Lib.Point import Point

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
    fg_color=(30,30,150)
    activated_fg_color=(100,100,250)

    def __init__(self):
        # Use self.keymap.set_next_keymap and self.keymap for stealing
        # keys when you are above the focus.
        self.keymap = Keymap()
        self.focus_keymap = Keymap()
        self.focus_keymap.obs_activation.add_observer(self, '_keymap_')
        self.keymap.set_next_keymap(self.focus_keymap)
        
        self._prev_frame_colors = []

        self._anim_pos = MovingValue(Point((0,0)), Point((0,00)))
        
    def _keymap_activated(self):
        self.got_focus()

    def _keymap_deactivated(self):
        self.lost_focus()

    def push_frame(self, frame_color=_dontchange, bg_color=_dontchange, fg_color=_dontchange):
        self._prev_frame_colors.append((self.frame_color, self.bg_color))
        if frame_color is not _dontchange:
            self.frame_color = frame_color
        if bg_color is not _dontchange:
            self.bg_color = bg_color
        if fg_color is not _dontchange:
            self.fg_color = fg_color

    def pop_frame(self):
        self.frame_color, self.bg_color, self.fg_color = self._prev_frame_colors.pop()
        
    def got_focus(self):
        self.push_frame(frame_color=self.activated_frame_color,
                        bg_color=self.activated_bg_color,
                        fg_color=self.activated_fg_color)

    def lost_focus(self):
        self.pop_frame()
        
    def draw(self, surface, pos):
        self._anim_pos.final = pos
        self._anim_pos.update()
        pos = self._anim_pos.current
        
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
