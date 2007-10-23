from __future__ import with_statement
from gui.main import pygame_display

with pygame_display((800, 600)) as display:
    from gui.Stack import Stack
    s = Stack()

    from gui.code.widget_for import widget_for
    from example import example
    s.push(widget_for(example))

    from gui.loop import loop

    from gui.code.KeysReflectionWidget import KeysReflectionWidget
    keys_reflection_widget = KeysReflectionWidget(loop.global_keymap)

    from observable.List import List
    from gui.Box import VBox
    from gui.Spacer import Spacer
    b = VBox(List([
        s,
#        Spacer((0, 50)),
#        keys_reflection_widget,
    ]), relay_focus=True)

    loop.loop(display, b)
