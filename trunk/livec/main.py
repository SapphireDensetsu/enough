# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from __future__ import with_statement
from codegui.main import pygame_display

import pygame

with pygame_display((800, 600), pygame.DOUBLEBUF) as display:
    from codegui.loop import loop
    from codegui.BrowserWidget import BrowserWidget

    from codegui.Namer import Namer
    from codegui.widget_for import widget_for
    loop.namer = Namer()
    
    from example import example
    loop.browser = BrowserWidget(widget_for(example))

    import pygame
    pygame.key.set_repeat(250,10)

    loop.loop(display, loop.browser)
