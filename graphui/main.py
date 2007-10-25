from __future__ import with_statement

import pygame
import contextlib
import draw

from Lib.Graph import Node, Edge

@contextlib.contextmanager
def pygame_display(*args, **kw):
    pygame.init()
    try:
        yield draw.set_mode(*args, **kw)
    except:
        import sys
        sys.last_type, sys.last_value, sys.last_traceback = sys.exc_info()
        import traceback
        traceback.print_exc()
        import pdb
        pdb.pm()
    finally:
        pygame.quit()

res = (800, 600)
with pygame_display(res, pygame.DOUBLEBUF) as display:
    from loop import loop
    from GraphWidget import GraphWidget
    from BrowserWidget import BrowserWidget

    b = BrowserWidget(GraphWidget((800,400)))
    loop.browser = b
    
    import pygame
    pygame.key.set_repeat(250,10)

    loop.loop(display, loop.browser)
