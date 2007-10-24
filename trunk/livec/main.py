from __future__ import with_statement
from gui.main import pygame_display

import pygame

with pygame_display((800, 600), pygame.DOUBLEBUF) as display:
    from gui.loop import loop

    from gui.code.BrowserWidget import BrowserWidget
    loop.browser = BrowserWidget()

    from gui.code.widget_for import widget_for
    from example import example
    loop.browser.push(widget_for(example))

    from gui.code.KeysReflectionWidget import KeysReflectionWidget
    keys_reflection_widget = KeysReflectionWidget(loop.global_keymap)

    from lib.observable.List import List
    from gui.Box import VBox
    from gui.Spacer import Spacer
    b = VBox(List([
        loop.browser,
        Spacer((0, 20)),
        keys_reflection_widget,
    ]), relay_focus=True)

    import pygame
    pygame.key.set_repeat(500,30)

    loop.loop(display, b)
