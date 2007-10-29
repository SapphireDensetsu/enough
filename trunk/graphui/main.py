# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from __future__ import with_statement

import pygame
import contextlib
from gui import draw
from gui.main import pygame_display

from lib.graph import Node, Edge

res = (800, 600)
with pygame_display(res, pygame.DOUBLEBUF) as display:
    from loop import loop
    from GraphWidget import GraphWidget
    from BrowserWidget import BrowserWidget
    loop.browser = BrowserWidget(GraphWidget((800,400)))
    
    import pygame
    pygame.key.set_repeat(250,10)

    loop.loop(display, loop.browser)
