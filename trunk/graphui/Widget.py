## /* Copyright 2007, Eyal Lotem, Noam Lewis, enoughmail@googlegroups.com */
## /*
##     This file is part of Enough.

##     Enough is free software; you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation; either version 3 of the License, or
##     (at your option) any later version.

##     Enough is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>.
## */

import pygame

from functools import partial

from Lib.Point import Point
from Lib import Func
from Lib.Font import find_font, get_font, lines_size
from guilib import get_default, MovingValue, ParamHolder

from Lib.Event import Event, TriggerList


def mouse_pos():
    return Point(pygame.mouse.get_pos())


class Widget(object):
    font_size = 40
    
    def __init__(self, text = '', pos=None, size=None, font_size=40):
        self.size = MovingValue(Point((20,20)), get_default(size, Point((20,20))))
        self.pos = MovingValue(Point((0,0)), get_default(pos, Point((0,0))), step=0.3)

        self.widgets = [] # sub-widgets
        self.focused_widgets = []
        self.hovered_widget = None
        self.trigger_lists = {'pre' : TriggerList(),
                              'post' : TriggerList(),}
                                  
        
        self.text = text
        self.font_size = font_size
        self.reset()
        
        self._init_params()
        self._init_event_triggers()

        from Ellipse import Ellipse
        self.shape = Ellipse(pygame.Rect(self.get_current_rect()))

    def reset(self):
        self.font=None
        self.default_font=None
        self.rendered_params = None
        self.rendered_text = None
        self.update_default_font()
        
    def __getstate__(self):
        d = self.__dict__.copy()
        del d['font']
        del d['default_font']
        del d['rendered_text']
        del d['rendered_params']
        return d
    def __setstate__(self, d):
        self.__dict__ = d
        self.reset()

    def update_default_font(self):
        self.default_font = get_font(self.font_size)

    def _init_params(self):
        self.params = ParamHolder(["visible", "enabled",
                                   "fore_color",
                                   "back_color",
                                   "text_color",
                                   "in_focus",
                                   "in_hover",
                                   "focus_back_color",
                                   "focus_text_color",
                                   "hover_back_color",
                                   "hover_text_color",
                                   "autosize",
                                   "user"], "WidgetParams")
        self.params.enabled = True
        self.params.visible = True
        self.params.fore_color = (100,100,200)
        self.params.back_color = (10,  10,15)
        self.params.text_color = (150,150,150)
        
        # If the widget is NOT really in focus, it will not receive
        # events. But this parameter specifies how to DISPLAY the
        # widget
        self.params.in_focus = False
        
        self.params.in_hover = False
        self.params.focus_back_color = (50,50,100)
        self.params.focus_text_color = (230,230,255)
        self.params.hover_back_color = (20,20,60)
        self.params.hover_text_color = (200,200,215)
        self.params.user = None
        self.params.autosize = "by size"

        
    def update_moving(self):
        self.render_text()
        self.size.update()
        self.pos.update()

    def in_bounds(self, pos):
        p = self.pos.current
        s = self.size.current
        if ((pos.x > p.x)
            and (pos.y > p.y)
            and (pos.x < p.x + s.x)
            and (pos.y < p.y + s.y)):
            return True
        return False
        
    def center_pos(self, current=True):
        if current:
            return self.pos.current+self.size.current*0.5
        return self.pos.final+self.size.final*0.5
        
    ######################################################################
    def add_widget(self, widget, z = None):
        if widget in self.widgets:
            raise ValueError("Widget already exists! %r" (widget,))

        if z is None:
            self.widgets.append(widget)
        else:
            self.widgets.insert(z, widget)

    def remove_widget(self, widget):
        self.widgets.remove(widget)
        
    def _z_ordered_widgets(self):
        return sorted((w.painting_z_order, w) for w in self.widgets)

    ######################################################################
    
    def handle_event(self, event):
        if self.trigger_lists['pre'].handle_event(event):
            return True

        if 'mouse' in event.type:
            orig_pos = event.pos.copy()
            event.pos += self.pos.current
        handled = False
        if event.to_all:
            for widget in self.widgets:
                handled = widget.handle_event(event)
        elif event.to_focused and self.focused_widgets:
            for widget in self.focused_widgets:
                handled = widget.handle_event(event)
        if 'mouse' in event.type:
            event.pos = orig_pos
        if handled:
            self.trigger_lists['post'].handle_event(event, only_forced=True)
            return True

        return self.trigger_lists['post'].handle_event(event)
            
    def _init_event_triggers(self):
        # force_handling = True means that the handler will be called
        # even if the event was handled by someone lower in the
        # hierarchy
        self.trigger_lists['pre'].register_event_type('paint', self.paint)
        for event_type, handler, force_handling in (('mouse motion', self.mouse_motion, False),
                                                    ('mouse down', self.mouse_down, False),
                                                    ('mouse up', self.mouse_up, False),
                                                    ('key up', self.key_up, False),
                                                    ('key down', self.key_down, False),
                                                    ):
            for when in ('pre', 'post'):
                # This saves for the common event handlers the need to
                # implement two methods
                self.trigger_lists[when].register_event_type(event_type, partial(handler, when), forced=force_handling)
            
    def mouse_motion(self, when, event):
        if when == 'post':
            return
        p = event.pos
        self.params.in_hover = True
        for z, widget in reversed(self._z_ordered_widgets()):
            if not widget.in_bounds(p):
                # todo call some widget.?? method?
                widget.params.in_hover = False
                continue
            
            if widget.mouse_motion(when, event):
                self.hovered_widget = widget
                return True
        return True

    def _modkey_used(self, key, mods=None):
        if not mods:
            mods = pygame.key.get_mods()
        return mods & key
    multiselect_modifier = pygame.KMOD_CTRL
    def _multiselect_modifier_used(self, mods=None):
        return self._modkey_used(self.multiselect_modifier)

    def mouse_down(self, when, event):
        if when == 'post':
            return
        p = event.pos
        self.params.in_focus = True
        if not self._multiselect_modifier_used():
            self.unset_focus()
            
        for z, widget in reversed(self._z_ordered_widgets()):
            if not widget.in_bounds(p):
                continue

            self.set_focus(widget)
            if widget.mouse_down(when, event):
                return True
        return True
        
    def mouse_up(self, when, event):
        pass
    def key_up(self, when, event):
        pass
    def key_down(self, when, event):
        pass

    def set_focus(self, widget):
        self.focused_widgets.append(widget)
        
    def unset_focus(self):
        for w in self.focused_widgets:
            w.params.in_focus = False
        self.focused_widgets = []

    ########################################################
    # TODO move this to some subclass

    def render_text(self):
        if self.params.in_focus:
            text_color = self.params.focus_text_color
        elif self.params.in_hover:
            text_color = self.params.hover_text_color
        else:
            text_color = self.params.text_color

        params = (self.params.autosize, tuple(self.size.final), self.text, text_color)
        if self.params.autosize == "by text":
            params += (self.default_font,)
        if self.rendered_params == params:
            return
            
        lines = self.text.split('\n')
        if self.params.autosize == "by size":
            does_fit, self.font = find_font(lines, tuple(self.size.final*(3./4)))
        else:
            self.font = self.default_font
            if self.params.autosize == "by text":
                width, height = lines_size(self.font, lines)
                self.size.final.x = self.size.current.x = width
                self.size.final.y = self.size.current.y = height

        rendered_lines = [self.font.render(line, True, text_color)
                          for line in lines]
        size = (max(t.get_width() for t in rendered_lines),
                sum(t.get_height() for t in rendered_lines))
        self.rendered_text = pygame.Surface(size, pygame.SWSURFACE|pygame.SRCALPHA|pygame.SRCCOLORKEY, 32)
        self.rendered_params = params
        
        # TODO: Support centering and stuff?
        y = 0
        for rline in rendered_lines:
            self.rendered_text.blit(rline, (0, y))
            y += rline.get_height()

    def get_current_rect(self):
        return self.pos.current.x, self.pos.current.y, self.size.current.x, self.size.current.y

    def paint(self, event):
        if not self.params.visible:
            return

        surface = event.surface
        
        self.update_moving()
        if self.params.in_focus:
            back_color = self.params.focus_back_color
        elif self.params.in_hover:
            back_color = self.params.hover_back_color
        else:
            back_color = self.params.back_color

        self.paint_shape(surface, back_color)
        self.paint_text(surface)

        self.paint_widgets(event)
        return True # since we are painting them explicitly, the lower widgets don't need to

    def paint_widgets(self, event):
        for z, widget in self._z_ordered_widgets():
            # We want to control the specific order of painting, so
            # don't let the standard event passing through the
            # hierarchy. just do it here
            widget.handle_event(event)
        
    def get_shape(self):
        # TODO make the shape a mutable attribute of self?
        self.shape.rect = pygame.Rect(self.get_current_rect())
        return self.shape
    
    def paint_shape(self, surface, back_color):
        # TODO use self.get_shape to paint our shape?
        pygame.draw.ellipse(surface, back_color, self.get_current_rect(), 0)
        if self.size.current.x > 5 and self.size.current.y > 5:
            # otherwise we get a pygame error for using a width that's larger than the elipse radius
            pygame.draw.ellipse(surface, self.params.fore_color, self.get_current_rect(), 2)


    def paint_text(self, surface):
        lines = self.text.split('\n')
        text_size = Point(lines_size(self.font, lines))
        surface.blit(self.rendered_text, tuple(self.center_pos()-text_size*0.5))

    def change_font_size(self, add = 0, mul = 1):
        self.font_size *= mul
        self.font_size += add
        self.default_font = get_font(self.font_size)
        

        

##    def mouse_down(self, e):
##        self.lock_focus(toggle=True)
##        if not self.dragging_enabled:
##            return
##        self.dragging = True
##        if self.focused_widgets:
##            self.drag_start_positions = [mouse_pos() - w.pos.current for w in self.focused_widgets]
        
##    def mouse_up(self, e):
##        self.unlock_focus()
##        self.dragging = False

##    def mouse_motion(self, e):
##        self.update_hover()
##        self.update_drag()
        
##    def _key_down(self, e):
##        pass

##    def update_drag(self):
##        p = mouse_pos()
##        if self.dragging:
##            if self.focused_widgets:
##                for w, d in zip(self.focused_widgets, self.drag_start_positions):
##                    w.pos.final = p - d

##    def lock_focus(self, toggle=False):
##        self.update_focus(toggle=toggle)
##        self.focus_locked = True
##    def unlock_focus(self):
##        self.focus_locked = False
##        #self.update_focus()
        
##    def update_focus(self, toggle=False):
##        if self.focus_locked:
##            return
##        p = mouse_pos()
##        for z, widget in reversed(self._z_ordered_widgets()):
##            if widget.in_bounds(p) and widget.params.enabled:
##                if not (pygame.key.get_mods() & self.multiselect_modifier):
##                    self.unset_focus()
##                self.set_focus(widget, toggle = toggle)
##                return
##        self.unset_focus()
        
##    def update_hover(self):
##        p = mouse_pos()
##        for z, widget in reversed(self._z_ordered_widgets()):
##            if widget.in_bounds(p) and widget.params.enabled:
##                self.set_hover(widget)
##                return
##        self.unset_hover()
        
##    def set_focus(self, widget, toggle = False):
##        if self.focused_widgets is None:
##            self.focused_widgets = []
##        if widget in self.focused_widgets:
##            if toggle:
##                widget.params.in_focus = False
##                self.focused_widgets.remove(widget)
##        else:
##            self.focused_widgets.append(widget)
##            widget.params.in_focus = True


##    def unset_hover(self):
##        if self.hovered_widget:
##            self.hovered_widget.params.in_hover = False
##        self.hovered_widget = None
##    def set_hover(self, widget):
##        self.unset_hover()
##        self.hovered_widget = widget
##        self.hovered_widget.params.in_hover = True
