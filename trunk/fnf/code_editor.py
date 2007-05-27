from gui.Lib.Point import Point
import gui
import code


import pygame

import string
from functools import partial

class CodeEditor(gui.Editor):
    def __init__(self, *args, **kw):
        super(CodeEditor, self).__init__(*args, **kw)
        self.widget_instance = {}
        self.widget_instance_reverse = {}
        self.instance_is_field = {}
        
        self.create_builtins()

    def create_builtins(self):
        fields = []
        for cls in code.builtins.builtins:
            fields.append(code.base.Field(cls, meta=dict(name=cls.meta['name'])))
            #self.create_instance(cls.create_instance())
        self.cls = code.base.Class(fields=fields, meta=dict(name='main'))
        self.instance = self.cls.create_instance()
        self.create_instance(self.instance)
    
    def create_instance(self, instance):
        self.create_instance_widgets(instance)
        self.relayout()

    def field_widgets_of_widget(self, widget):
        instance = self.widget_instance[widget]
        for field_instance in instance.field_instances():
            if field_instance in self.widget_instance_reverse:
                yield self.widget_instance_reverse[field_instance]
        
    def relayout(self):
        if self._dont_layout:
            return
        gui.base.reorder(self.widgets)
        #widgets = [widget for widget in self.widgets if not widget.order.ignore]
        #gui.layouts.TableLayout(self.width, self.height, widgets, scale =self.scale, autoscale = True)
        widget = self.widget_instance_reverse[self.instance]
        widget.pos = Point(self.width/2, self.height/2)
        gui.layouts.SurroundLayout(self.width, self.height, widget,
                                   self.field_widgets_of_widget, scale=self.scale)
        
    def create_instance_widgets(self, instance, level=0, field=None):
        #print instance
        if instance in self.widget_instance_reverse:
            # Widget exists Already
            return self.widget_instance_reverse[instance]
        
        w = gui.Widget(Point(15,15))
        w.order.level = level
        field_instances_by_name = instance.field_instances_by_name()

        self.add_instance_widget(instance, w, field)
        self.update_widget(w, instance)
        
        for field in instance.cls.fields:
            field_instance = field_instances_by_name[field.meta['name']]
            field_widget = self.create_instance_widgets(field_instance, level+1, field)
            w.node.connect_out(field_widget.node)

        return w
    
    def add_instance_widget(self, instance, widget, field=None):
        self.widget_instance[widget] = instance
        self.widget_instance_reverse[instance] = widget
        self.instance_is_field[instance] = field
        
        instance.event_field_instance_replaced.register(partial(self.instance_replaced, instance))
        instance.event_modified.register(partial(self.instance_modified))
        
        self.add_widget(widget)
        
    def replace_instance(self, old_instance, new_instance):
        #print 'replacing', old_instance, new_instance
        if old_instance is new_instance:
            return
            
        widget = self.widget_instance_reverse[old_instance]
        old_in_connections = list(widget.node.connections['in'])
        self.remove_instance(old_instance)
        
        field = self.instance_is_field.get(old_instance, None)
        new_widget = self.create_instance_widgets(new_instance, level=widget.order.level, field=field)
        new_widget.pos = (widget.pos + new_widget.pos)*0.5
        for old_in in old_in_connections:
            new_widget.node.connect_in(old_in)
        
    def remove_instance(self, instance):
        widget = self.widget_instance_reverse[instance]
        self.remove_widget(widget)
        del self.widget_instance[widget]
        del self.widget_instance_reverse[instance]
        del self.instance_is_field[instance]
        for field in instance.cls.fields:
            field_instance = field_instances_by_name[field.meta['name']]
            self.remove_instance(field_instance)

    def instance_replaced(self, instance, field, old_field_instance, new_field_instance, modified_by):
        if old_field_instance is None:
            self.create_instance_widgets(new_field_instance, field=field)
        else:
            self.replace_instance(old_field_instance, new_field_instance)
        self.update_widgets()

    def instance_modified(self, instance, modified_by):
        if instance not in self.widget_instance_reverse:
            return
        w = self.widget_instance_reverse[instance]
        self.update_widget(w, instance)

    def update_widgets(self):
        for w in self.widgets:
            i = self.widget_instance[w]
            self.update_widget(w, i)
            
    def update_widget(self, w, instance):
        field = self.instance_is_field.get(instance, None)
        if field:
            name = field.meta['name']
        else:
            name = instance.cls.meta['name']
        value = str(instance.meta.get('value', ''))
        w.set_text_line(0, name)
        w.set_text_line(1, value)

    def connect_widgets_permanently(self, w1, w2):
        i1 = self.widget_instance[w1]
        i2 = self.widget_instance[w2]
        if i1.cls != i2.cls:
            return

        #super(CodeEditor, self).connect_widgets_permanently(w1, w2)
        sf1 = self.instance.subfield_hierarchy_by_instance(i1)
        sf2 = self.instance.subfield_hierarchy_by_instance(i2)
        self.cls.union(sf1, sf2)
        self.update_widgets()
        
        
    def key_up(self, e):
        if e.mod & pygame.KMOD_CTRL:
            if e.key == pygame.K_BACKSPACE:
                i = self.widget_instance[self.hovered_widget]
                sf = self.instance.subfield_hierarchy_by_instance(i)
                self.cls.split(sf)
                
        else:
            if not self.hovered_widget:
                return
            k = e.key
            if not (0 <= k and k < 256):
                return
            self.printable_key_up(k)

    def printable_key_up(self, k):
        t = self.hovered_widget.text_lines[1]
        if t is None:
            t = ''

        ch = chr(k)
        if k == pygame.K_BACKSPACE:
            t = t[:-1]
        elif ch not in string.printable:
            return
        else:
            t += ch
        
        i = self.widget_instance[self.hovered_widget]
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
        #self.update_widgets()
        #self.hovered_widget.set_text()
        
            

    

import random

def test():
    a = CodeEditor()
    a.run()

if __name__=='__main__':
    test()
    
