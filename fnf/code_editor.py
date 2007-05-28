from gui.Lib.Point import Point
import gui
import code


import pygame

import string
from functools import partial



class InstanceWidget(gui.Widget):
    # todo use a weak list
    all_widgets = []
    
    def __init__(self, instance, level=0, is_field=None, add_widget_handler=None, del_widget_handler=None, **kw):
        super(InstanceWidget, self).__init__(Point(15,15), **kw)
        self.order.level = level
        
        self.add_widget_handler=add_widget_handler
        self.del_widget_handler=del_widget_handler
        
        self.instance = instance
        self.is_field = is_field

        self.instance.event_field_instance_set.register(self.handle_field_instance_set)
        self.instance.event_field_instance_removed.register(self.handle_field_instance_removed)
        self.instance.event_modified.register(self.handle_instance_modified)
        self.instance.event_field_instance_linked.register(self.handle_subfields_linked)
        
        self.field_instance_widget_by_field = {}
        self.field_instances_by_field_widgets = {}
        
        field_instances_by_name = instance.field_instances_by_name()
        for field in instance.cls.fields:
            field_instance = field_instances_by_name[field.meta['name']]
            self.create_field(field, field_instance)

        self.update()
        self.add_widget_handler(self)

        # A class-wide list
        self.all_widgets.append(self)

    @classmethod
    def from_code_class(cls, code_class, **kw):
        return cls(code_class.create_instance(), **kw)

    def create_field(self, field, field_instance):
        field_widget = type(self)(field_instance, self.order.level+1, is_field = field,
                                  add_widget_handler=self.add_widget_handler,
                                  del_widget_handler=self.del_widget_handler)

        field_widget.order.sublevel = len(self.field_instance_widget_by_field.keys())
        
        self.field_instance_widget_by_field[field] = field_widget
        self.field_instances_by_field_widgets.setdefault(field_widget, []).append(field)
        self.node.connect_out(field_widget.node)


    def delete_field(self, field, field_instance):
        field_instance_widget = self.field_instance_widget_by_field[field]
        self.field_instances_by_field_widgets[field_instance_widget].remove(field)
        del self.field_instance_widget_by_field[field]
        self.node.disconnect(field_instance_widget.node)

        field_instance_widget.layout_hint_node.disconnect_all()
        
        if not self.field_instances_by_field_widgets[field_instance_widget]:
            del self.field_instances_by_field_widgets[field_instance_widget]
            self.del_widget_handler(field_instance_widget)


    def handle_field_instance_set(self, instance, field, field_instance):
        assert self.instance == instance
        
        field_widget = self.field_instance_widget_by_field.get(field, None)
        if field_widget:
            if field_widget.instance != field_instance:
                field_widget.instance = field_instance
                field_widget.layout_hint_node.disconnect_all()
            return
        self.create_field(field, field_instance)


    def handle_field_instance_removed(self, instance, field, field_instance):
        assert self.instance == instance

        field_widget = self.field_instance_widget_by_field.get(field, None)
        if field_widget.instance != field_instance:
            # The field was linked and the widget was already updated. nothing to do
            return
        
        self.delete_field(field, field_instance)

    def handle_instance_modified(self, subfield_instance, modified_by):
        self.update()

    def handle_subfields_linked(self, instance, removed_subfield_instance, new_subfield_instance):
        all_widgets = list(self.all_widgets)
        
        # Each instance could have several widgets displaying it
        for subfield_widget1 in all_widgets:
            if subfield_widget1.instance == new_subfield_instance:
                for subfield_widget2 in all_widgets:
                    if subfield_widget2.instance == removed_subfield_instance:
                        subfield_widget1.layout_hint_node.connect_out(subfield_widget2.layout_hint_node)
                        subfield_widget2.instance = subfield_widget1.instance
        
    def update(self):
        if self.is_field:
            name = self.is_field.meta['name']
        else:
            name = self.instance.cls.meta['name']
        value = str(self.instance.meta.get('value', ''))
        self.set_text_line(0, name)
        self.set_text_line(1, value)

    def iter_field_widgets(self):
        for field_widget in self.field_instances_by_field_widgets.keys():
            yield field_widget

    def connect_subfields(self, subfield_widget1, subfield_widget2):
        sf1 = self.instance.subfield_hierarchy_by_instance(subfield_widget1.instance)
        sf2 = self.instance.subfield_hierarchy_by_instance(subfield_widget2.instance)

        # This will cause all proper creation/removal events to occur
        self.instance.cls.union(sf1, sf2)

        

    def disconnect_subfield(self, subfield_widget):
        sf = self.instance.subfield_hierarchy_by_instance(subfield_widget.instance)
        self.instance.cls.split(sf)

    def handle_key(self, key):
        i = self.instance
        if len(self.text_lines) < 2:
            t = ''
        else:
            t = self.text_lines[1]

        if key == pygame.K_BACKSPACE:
            t = t[:-1]
        else:
            t += chr(key)
            
        if i.cls == code.builtins.fnf_number:
            if not t:
                t = '0'
            try:
                value = float(t)
            except:
                return
            if value == int(value):
                value = int(value)
            i.meta['value'] = value
            i.self_modified(i)
        else:
            self.hovered_widget.set_text_line(0, t)
        

class CodeEditor(gui.Editor):
    def __init__(self, *args, **kw):
        super(CodeEditor, self).__init__(*args, **kw)
        self.main_widget = None
        self.top_level_widget = InstanceWidget.from_code_class(code.builtins.builtins_cls,
                                                               add_widget_handler=self.add_widget,
                                                               del_widget_handler=self.remove_widget)

        self.set_main_widget(self.top_level_widget)

    def set_main_widget(self, widget):
        self.main_widget = widget
        widget.visible = False

    def field_widgets_of_widget(self, widget):
        for f in widget.iter_field_widgets():
            yield f
            
    def relayout(self):
        if self._dont_layout:
            return
        
        # TODO fix reorder - probably need to change the way we do it..
        self.reorder()
        #widgets = [widget for widget in self.widgets if not widget.order.ignore]
        #gui.layouts.TableLayout(self.width, self.height, widgets, scale =self.scale, autoscale = True)

        if self.main_widget is None:
            return

        field_widgets = list(sorted((w.order.sublevel, w) for w in self.main_widget.iter_field_widgets()))
        margin = 10
        x = margin
        step = self.width/float(len(field_widgets))
        for sublevel, widget in field_widgets:
            widget.pos = Point(x, 130)
            x += step + margin
            gui.layouts.SurroundLayout(step, self.height, widget,
                                       self.field_widgets_of_widget, scale=self.scale)
        
    
    def update_widgets(self):
        for w in self.widgets:
            w.update()

    def connect_widgets_permanently(self, w1, w2):
        self.main_widget.connect_subfields(w1, w2)
        self.update_widgets()
        
        
    def key_up(self, e):
        if e.mod & pygame.KMOD_CTRL:
            if e.key == pygame.K_BACKSPACE:
                self.main_widget.disconnect_subfield(self.hovered_widget)
                
        else:
            if not self.hovered_widget:
                return
            k = e.key
            if not (0 <= k and k < 256):
                return
            self.printable_key_up(k)

    def printable_key_up(self, k):
        self.hovered_widget.handle_key(k)
        self.update_widgets()
            

    

import random

def test():
    a = CodeEditor()
    a.run()

if __name__=='__main__':
    test()
    
