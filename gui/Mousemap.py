# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from Lib.Point import Point
import pygame

class MouseEvent(object):
    def __init__(self, pygame_mouse_event):
        self.type = pygame_mouse_event.type
        self.pos = Point(pygame_mouse_event.pos)
        
class MouseArea(object):
    def __init__(self, in_bounds):
        self.in_bounds = in_bounds

class MouseMap(object):
    def __init__(self):
        self.mouse_areas = []
        self.area_to_handler = {}

    def mouse_event(self, event):
        p = event.pos
        for mouse_area, handler in self.mouse_areas:
            if mouse_area.in_bounds(p):
                handler(event)

    def push_area(self, mouse_area, handler):
        assert mouse_area not in self.area_to_handler
        # TODO make intelligent code that intersects areas for optimal finding
        self.area_to_handler[handler] = mouse_area
        self.mouse_areas.insert(0, (mouse_area, handler))
    def remove_area(self, area):
        handler = self.area_to_handler[area]
        self.mouse_areas.remove((area, handler))
        del self.area_to_handler[area]
                

    
