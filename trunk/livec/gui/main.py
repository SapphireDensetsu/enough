import pygame
import contextlib
import gui.draw

@contextlib.contextmanager
def pygame_display(*args, **kw):
    pygame.init()
    try:
        yield gui.draw.set_mode(*args, **kw)
    except:
        import sys
        sys.last_type, sys.last_value, sys.last_traceback = sys.exc_info()
        import traceback
        traceback.print_exc()
        import pdb
        pdb.pm()
    finally:
        pygame.quit()
