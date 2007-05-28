import pygame

from Lib.Point import Point
from Lib.AttrDict import AttrDict
from Lib import Graph, Func

import layouts

def mouse_pos():
    x,y = pygame.mouse.get_pos()
    return Point(x,y)

def Event(name, **kw):
    return pygame.event.Event(pygame.USEREVENT, name=name, **kw)

# ________________________________________________________________________

class Order(AttrDict):
    allowed_fields = [('level',0),
                      ('sublevel',0),
                      ('ignore', False),
                      ]
    
class Widget(object):
    def __init__(self, size, pos = None, order=None, hover_color=(120,120,250), unhover_color=(20,20,150)):
        if pos is None:
            pos = Point(0,0)
        if order is None:
            order = Order()
        self.target_pos = pos.shallow_copy()
        self._size = size
        self.order = order
        self._pos = pos.shallow_copy()
        self.target_scale = 1
        self._scale = 1

        self.visible = True
        self.size_margin = 10
        self.speed = Point(0.1,0.1)
        self.scale_speed = 0.1
        self.autogrow_to_fit_text = True
        self.rendered_text_lines = None
        self.text_lines = []
        self._target_size = self._size.shallow_copy()
        
        self.font_size = 12
        self._prev_font_scale = 12
        self._prev_text_lines = self.text_lines[:]

        # node for topology
        self.node = Graph.Node(self)
        # node for layout hints
        self.layout_hint_node = Graph.Node(self)
        
        self.update_font()

        self.hover_color = hover_color
        self.unhover_color = unhover_color
        self.border_color = hover_color
        self.hover_out()

        self.accel = Point(0,0)
        self.vel = Point(0,0)
        
    def in_bounds(self, pos):
        s = self._scaled_size()
        if ((pos.x > self._pos.x)
            and (pos.y > self._pos.y)
            and (pos.x < self._pos.x + s.x)
            and (pos.y < self._pos.y + s.y)):
            return True
        return False

    def set_pos(self, pos):
        self.target_pos = pos.shallow_copy()
    def get_pos(self):
        return self.target_pos
    pos = property(get_pos, set_pos)

    def set_scale(self, scale):
        self.target_scale = scale
        self.update_target_text_scale()
    def get_scale(self):
        return self.target_scale
    scale = property(get_scale, set_scale)

    def set_size(self, size):
        self._size = size/self.target_scale
    def get_size(self):
        if not self.text_lines:
            return self._size*self.target_scale
        return self._target_size
    size = property(get_size, set_size)
    
    def update_pos(self):
        #self._pos += (self.target_pos - self._pos)*self.speed
        self.accel = (self.target_pos - self._pos)*self.speed
        for puller in self.layout_hint_node.connections['out']:
            w = puller.value
            self.accel += (w._pos - self._pos)*0.2
        for puller in self.layout_hint_node.connections['in']:
            w = puller.value
            self.accel += (w._pos - self._pos)*0.2
            
        self.vel = self.accel # todo +=
        self._pos += self.vel

    def update_scale(self):
        self._scale += (self.target_scale - self._scale)*self.scale_speed
        self.update_font()
        #print self._scale

    def update_font(self):
        if not self.text_lines:
            return
        font_scale = int(self.font_size*self._scale*2)
        if (self.text_lines == self._prev_text_lines) and (font_scale == self._prev_font_scale):
            return
        self._prev_text_lines = self.text_lines
        self._prev_font_scale = font_scale
        
        self.font = self.get_font(font_scale)
        self.rendered_text_lines = []
        mw, mh = 0, 0
        linesize = self.font.get_linesize()
        
        for i, line in enumerate(self.text_lines):
            rendered_line = self.font.render(line, True, (250,250,250,150))
            self.rendered_text_lines.append((rendered_line, linesize*i))
            w,h = self.font.size(line)
            mw = max(mw, w)
            mh += linesize
        if self.autogrow_to_fit_text:
            self._size = Point(mw, mh)
            
        
    def _scaled_size(self):
        if not self.text_lines:
            return self._size*self._scale
        return self._size
    
    def paint(self, surface):
        if not self.visible:
            return
        #self.set_text(str(self.order.sublevel))
        self.update_scale()
        self.update_pos()
        s = self._scaled_size()

        self.draw_connections(surface)

        pygame.draw.rect(surface, self.color, (self._pos.x, self._pos.y, s.x, s.y), 0)
        pygame.draw.rect(surface, self.border_color, (self._pos.x, self._pos.y, s.x, s.y), 2)
        #pygame.draw.ellipse(surface, self.color, (self._pos.x, self._pos.y, s.x, s.y), 3)
        if self.rendered_text_lines:
            for rendered_text_line, y in self.rendered_text_lines:
                surface.blit(rendered_text_line, (self._pos.x, self._pos.y+y))

    def draw_connections(self, surface):
        s = self._scaled_size()
        my_pos = self._pos + Point(s.x/2, s.y/2)
        for widget_node in self.node.connections['out']:
            widget = widget_node.value
            other_pos = widget._pos + Point(widget._scaled_size().x/2, widget._scaled_size().y/2)
            pygame.draw.aalines(surface, (200,220,250,100), False, (my_pos.as_tuple(), other_pos.as_tuple()), True)

        for l in self.layout_hint_node.connections.values():
            for widget_node in l:
                widget = widget_node.value
                other_pos = widget._pos + Point(widget._scaled_size().x/2, widget._scaled_size().y/2)
                pygame.draw.aalines(surface, (200,20,50,100), False, (my_pos.as_tuple(), other_pos.as_tuple()), True)

    @staticmethod
    @Func.cached
    def get_font(font_size):
        return pygame.font.SysFont('serif',font_size)

    def update_target_text_scale(self):
        if not self.text_lines:
            return
        mw,mh = 0,0
        for line in self.text_lines:
            w,h = self.get_font(int(self.font_size*self.target_scale*2)).size(line)
            mw = max(mw, w)
            mh += h
        self._target_size = Point(mw,mh)
        
    def set_text(self, text_lines):
        self.text_lines = text_lines[:]
        if not self.text_lines:
            self.rendered_text_lines = []
            return
        
        self.update_target_text_scale()
        self.update_font()

    def set_text_line(self, num, line):
        if num >= len(self.text_lines):
            self.text_lines.extend(['']*(num-len(self.text_lines)+1))
        self.text_lines[num] = line
        self.set_text(self.text_lines)

    def hover_in(self):
        self.color = self.hover_color

    def hover_out(self):
        self.color = self.unhover_color
# ________________________________________________________________________

## def update_sublevel(node, val, dfs=False):
##     node.value.order.sublevel = val
##     nodes_left = [(i,other) for (i,other) in enumerate(node.connections['out'])]
##     i = 0
##     level = 0
##     while nodes_left:
##         val, other = nodes_left.pop(0)
##         if other.value.order.ignore:
##             continue
        
##         if other.value.order.level > level:
##             level = other.value.order.level
##             i = 0
            
##         other.value.order.sublevel = val
##         for subother in other.connections['out']:
##             if dfs:
##                 nodes_left.insert(0,(i,subother))
##             else:
##                 nodes_left.append((i,subother))
##             i += 1

            
##def update_topological_levels(widgets):
##    nodes = [widget.node for widget in widgets]
##     ordered = Graph.topological_sort(nodes)
##     for level, node in ordered:
##         node.value.order.level = level


##     # set the sublevel for each family of connected nodes so that drawing them together will be easier
##     for i, (level, node) in enumerate(ordered):
##         if level > 0:
##             break
##         update_sublevel(node, i)

def find_widget_of_near_order(widgets, level, sublevel):
    for widget in widgets:
        if widget.order.level == level and widget.order.sublevel == sublevel:
            return widget

    for widget in widgets:
        if widget.order.level == level:
            return widget

    return widgets[0]
        
    
class App(object):
    def __init__(self, width=800, height=600, flags=0):
        self.width = width
        self.height = height
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((width,height),flags)
        self.widgets = []
        self.z_ordered = []
        self.z = 0
        self.stop = False
        self.pygame_handlers = {}
        self.scale = 1

        self.hovered_widget = None
        self._hover_only_on_motion = False


        self.my_handlers = {'paint': [self._paint,]}
        for pg_type, handler in ((pygame.KEYUP, self._key_up),
                                 (pygame.MOUSEBUTTONDOWN, self._mouse_down),
                                 (pygame.MOUSEBUTTONUP, self._mouse_up),
                                 (pygame.MOUSEMOTION, self._mouse_motion),
                                 (pygame.USEREVENT, self._handle_my_event),
                                 ):
            self.register_pygame_event(pg_type, handler)
            
        self._dont_layout = False
        self._sublevel = 0
        
    def post_event(self, event):
        pygame.event.post(event)
        
    def add_widget(self, widget, z = None):
        if z is None: z = self.z
        self.z += 1
        self.widgets.append(widget)
        widget.order.sublevel = self._sublevel
        self._sublevel += 1
        self.z_ordered.append((z, widget))
        self.z_ordered.sort()
        self.post_event(Event('paint'))
        self.relayout()

    def remove_widget(self, widget):
        self.widgets.remove(widget)
        widget.node.disconnect_all()
        for i, (z, w) in enumerate(self.z_ordered[:]):
            if w == widget:
                self.z_ordered.pop(i)
                break
            
    def reorder(self):
        widgets = self.widgets
        levels = {}
        for widget in widgets:
            levels.setdefault(widget.order.level, []).append((widget.order.sublevel, widget))


        for i, level in enumerate(sorted(levels.keys())):
            level_widgets = levels[level]
            for j, (sublevel, widget) in enumerate(sorted(level_widgets)):
                widget.order.level = i
                widget.order.sublevel = j

        
    def relayout(self):
        if self._dont_layout:
            return
        self.reorder()
        widgets = [widget for widget in self.widgets if not widget.order.ignore]
        layouts.TableLayout(self.width, self.height, widgets, scale =self.scale, autoscale = True)
        

    def register_pygame_event(self, pg_type, handler):
        self.pygame_handlers.setdefault(pg_type, []).append(handler)

    def register_event(self, name, handler):
        self.my_handlers.setdefault(name, []).append(handler)

    def _handle_my_event(self, e):
        if e.name not in self.my_handlers:
            return
        for handler in self.my_handlers[e.name]:
            handler(e)
        
    def handle_event(self, e):
        if e.type is pygame.QUIT: self.quit()
        elif e.type is pygame.KEYDOWN and e.key == pygame.K_ESCAPE: self.quit()

        if e.type in self.pygame_handlers:
            for handler in self.pygame_handlers[e.type]:
                handler(e)

    def quit(self):
        self.stop = True

    def run(self):
        while not self.stop:
            pygame.event.pump()
            self.handle_events()

    def handle_events(self):
        events = pygame.event.get()
        if not self._hover_only_on_motion:
            self._update_hover()
        self._paint(None)
        for event in events:
            self.handle_event(event)
        #if not event or event == pygame.NOEVENT:
        #    return

    def connect_widgets(self, from_w, to_w):
        from_w.node.connect_out(to_w.node)
        self.relayout()

    def disconnect_widgets(self, w1, w2):
        w1.node.disconnect(w2.node)
        self.relayout()

    def widgets_connected(self, w1, w2):
        return w1.node.is_connected(w2.node)
    # ________________________________
    
    def _paint(self, event):
        self.screen.fill((0,0,0))
        for z_order, widget in self.z_ordered:
            widget.paint(self.screen)
        pygame.display.flip()


    def _key_up(self, e):
        # The user is editing with the keyboard, don't disturb by hovering out!
        self.lock_hover()
        
        if (e.mod & pygame.KMOD_CTRL):
            if e.key == pygame.K_w:
                self.scale += 0.3
                self.relayout()
            elif e.key == pygame.K_q:
                self.scale -= 0.3
                self.relayout()
            elif e.key == pygame.K_LEFT:
                if self.hovered_widget:
                    self.hovered_widget.order.sublevel -= 1.5
                self.relayout()
            elif e.key == pygame.K_RIGHT:
                if self.hovered_widget:
                    self.hovered_widget.order.sublevel += 1.5
                self.relayout()
            elif e.key == pygame.K_UP:
                if self.hovered_widget:
                    self.hovered_widget.order.level -= 1
                self.lock_hover()
                self.relayout()
            elif e.key == pygame.K_DOWN:
                if self.hovered_widget:
                    self.hovered_widget.order.level += 1
                self.relayout()
        else:
            if e.key == pygame.K_LEFT:
                if self.hovered_widget:
                    self.hover(find_widget_of_near_order(self.widgets,
                                                         self.hovered_widget.order.level,
                                                         self.hovered_widget.order.sublevel - 1))
                else:
                    self.hover_first()
            elif e.key == pygame.K_RIGHT:
                if self.hovered_widget:
                    self.hover(find_widget_of_near_order(self.widgets,
                                                         self.hovered_widget.order.level,
                                                         self.hovered_widget.order.sublevel + 1))
                else:
                    self.hover_first()
            elif e.key == pygame.K_UP:
                if self.hovered_widget:
                    self.hover(find_widget_of_near_order(self.widgets,
                                                         self.hovered_widget.order.level - 1,
                                                         self.hovered_widget.order.sublevel))
                else:
                    self.hover_first()
            elif e.key == pygame.K_DOWN:
                if self.hovered_widget:
                    self.hover(find_widget_of_near_order(self.widgets,
                                                         self.hovered_widget.order.level + 1,
                                                         self.hovered_widget.order.sublevel))
                else:
                    self.hover_first()

    def hover_first(self):
        self.hover(find_widget_of_near_order(self.widgets, 0, 0))
        
    def _mouse_down(self, e):
        pass

    def _mouse_up(self, e):
        pass

    def _mouse_motion(self, e):
        self._update_hover()
        self.unlock_hover()
        
    def _update_hover(self):
        p = mouse_pos()
        for widget in self.widgets:
            if widget.in_bounds(p):
                self.hover(widget)
                return
        
        self.unhover()

    def hover(self, widget):
        self.unhover()
        self.hovered_widget = widget
        widget.hover_in()
        
    def unhover(self):
        if not self.hovered_widget:
            return
        self.hovered_widget.hover_out()
        self.hovered_widget = None
            
    def lock_hover(self):
        # Causes the hover to remain on the given widget until the mouse moves
        # (even if widgets move around)
        self._hover_only_on_motion = True

    def unlock_hover(self):
        if self._hover_only_on_motion:
            self.relayout()
        self._hover_only_on_motion = False

    def lock_positions(self):
        self._dont_layout = True
    def unlock_positions(self):
        self._dont_layout = False
        
# ________________________________________________________________________

import random

def test():
    a = App()
    for i in xrange(1):
        w = Widget(Point(20-i,20+i), pos=Point(15*i,23*i), order=Order(i/3))
        a.add_widget(w)
    a.run()

if __name__=='__main__':
    test()
    
