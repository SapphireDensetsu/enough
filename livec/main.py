from __future__ import with_statement
from gui.main import pygame_display

with pygame_display((800, 600)) as display:
    from gui.Stack import Stack
    s = Stack()

    from gui.code.widget_for import widget_for
    from example import example
    s.push(widget_for(example))
    from gui.loop import loop
    loop.loop(display, s)
