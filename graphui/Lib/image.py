
from Func import cached
import pygame

@cached
def load_image(filename):
    return pygame.image.load(filename)

@cached
def _cached_scale(surface, (w,h)):
    return pygame.transform.scale(surface, (w,h))

def fast_scale(surface, (w,h), delta=1):
    w = (w // delta) * delta
    h = (h // delta) * delta
    return _cached_scale(surface, (w,h))
