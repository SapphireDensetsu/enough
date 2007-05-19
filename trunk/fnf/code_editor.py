from gui.Lib.Point import Point
import gui
import code


import pygame
import string



class CodeEditor(gui.Editor):
    def __init__(self, *args, **kw):
        super(CodeEditor, self).__init__(*args, **kw)
        self.widget_instance = {}
        self.widget_instance_reverse = {}
        
        self.create_builtins()

    def create_builtins(self):
        fields = []
        for cls in code.builtins.builtins:
            fields.append(code.base.Field(cls, meta=dict(name='builtin_'+cls.meta['name'])))
            #self.create_instance(cls.create_instance())
        self.cls = code.base.Class(fields=fields, meta=dict(name='main'))
        self.instance = self.cls.create_instance()
        self.create_instance(self.instance)
    
    def create_instance(self, instance):
        self.create_instance_widgets(instance)
        self.relayout()

    def create_instance_widgets(self, instance, level=0):
        #print instance
        w = gui.Widget(Point(15,15))
        w.order.level = level
        field_instances_by_name = instance.field_instances_by_name()

        self.add_instance_widget(instance, w)
        self.update_widget(w, instance)
        
        for field in instance.cls.fields:
            field_instance = field_instances_by_name[field.meta['name']]
            field_widget = self.create_instance_widgets(field_instance, level+1)
            w.node.connect_out(field_widget.node)

        return w
    
    def add_instance_widget(self, instance, widget):
        self.widget_instance[widget] = instance
        self.widget_instance_reverse[instance] = widget
        try:
            instance.event_modified.register(self.instance_modified)
        except AssertionError:
            # todo fix
            pass
        self.add_widget(widget)
        
    def replace_instance(self, old_instance, new_instance):
        if old_instance is new_instance:
            return
        widget = self.widget_instance_reverse[old_instance]
        old_in_connections = list(widget.node.connections['in'])
        self.remove_instance(old_instance)
        new_widget = self.create_instance_widgets(new_instance, widget.order.level)
        for old_in in old_in_connections:
            new_widget.node.connect_in(old_in)
        
        
    def remove_instance(self, instance):
        widget = self.widget_instance_reverse[instance]
        self.remove_widget(widget)
        del self.widget_instance[widget]
        del self.widget_instance_reverse[instance]
        for field in instance.cls.fields:
            field_instance = field_instances_by_name[field.meta['name']]
            self.remove_instance(field_instance)

    def instance_modified(self, instance, field, old_field_instance, new_field_instance, self_modified):
        if old_field_instance is not None and new_field_instance is not None:
            self.replace_instance(old_field_instance, new_field_instance)
        self.update_widgets()

    def update_widgets(self):
        for w in self.widgets:
            i = self.widget_instance[w]
            self.update_widget(w, i)
            
    def update_widget(self, w, instance):
        text = str(instance.meta.get('value', instance.cls.meta['name']))
        w.set_text(text)

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
        if not e.mod & pygame.KMOD_CTRL:
            if not self.hovered_widget:
                return
            k = e.key
            if not (0 <= k and k < 256):
                return
            self.printable_key_up(k)

    def printable_key_up(self, k):
        t = self.hovered_widget.text
        if t is None:
            t = ''

        ch = chr(k)
        if k == pygame.K_BACKSPACE:
            t = t[:-1]
        elif ch in string.printable:
            t += ch
        else:
            return
        
        i = self.widget_instance[self.hovered_widget]
        if i.cls == code.builtins.fnf_number:
            if not t:
                t = '0'
            try:
                value = int(t)
            except ValueError:
                try:
                    value = float(t)
                except ValueError:
                    return
            i.meta['value'] = value
            i.self_modified(i)
            
        #self.update_widgets()
        #self.hovered_widget.set_text()
        
            

    

import random

def test():
    a = CodeEditor()
    a.run()

if __name__=='__main__':
    test()
    
