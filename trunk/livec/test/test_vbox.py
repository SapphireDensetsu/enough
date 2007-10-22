from __future__ import with_statement
import fix_import_paths
from gui.Box import VBox
from gui.TextEdit import TextEdit
from gui.main import pygame_display
from observable.List import List

def main():
    with pygame_display((800, 600)) as display:
        v = VBox(List([
            TextEdit(lambda : 'Moshiko!'),
            TextEdit(lambda : 'Dani!'),
            TextEdit(lambda : 'Yosefa!'),
            TextEdit(lambda : 'Yekutiel!'),
        ]))
        from gui.loop import loop
        loop.loop(display.subsurface(10,10,500,500), v)

if __name__ == '__main__':
    main()
