# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import pygame

def get_font(font_size):
    return pygame.font.SysFont(pygame.font.get_default_font(), int(font_size))

pygame.font.init()
fonts = list(
    get_font(i**1.1)
    for i in xrange(5, 100)
)

def approximate_binary_search(items, cmp):
    if not items:
        raise IndexError("Cannot find matching item")
    if len(items) == 1:
        return items[0]
    mid = len(items)//2
    item = items[mid]
    c = cmp(item)
    if c > 0:
        return approximate_binary_search(items[:mid], cmp)
    elif c < 0:
        return approximate_binary_search(items[mid:], cmp)
    else:
        return item

def lines_size(font, lines):
    if not lines:
        return (0, 0)
    height = font.get_height() * len(lines)
    width = max(font.size(line)[0] for line in lines)
    return width, height

def find_font(lines, (max_width, max_height)):
    def does_fit(font):
        width, height = lines_size(font, lines)
        if height > max_height or width > max_width:
            return 1
        return -1
    font = approximate_binary_search(fonts, does_fit)
    return does_fit(font) == -1, font
