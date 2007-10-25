# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from __future__ import with_statement
from gui.main import pygame_display

import pygame

with pygame_display((800, 600), pygame.DOUBLEBUF) as display:
    from gui.loop import loop
    from gui.code.BrowserWidget import BrowserWidget

    from gui.code.Namer import Namer
    loop.namer = Namer()
    
    from example import example
    loop.browser = BrowserWidget(example)

    import pygame
    pygame.key.set_repeat(250,10)

    loop.loop(display, loop.browser)
