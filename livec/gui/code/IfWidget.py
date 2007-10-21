from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for, ccode_widget_for

from CacheMap import CacheMap
from List import List

from itertools import chain

def cached_widget_for(items):
    return CacheMap(widget_for, List(items))

def tabbed(widget):
    b = HBox(List([widget_for(' '), widget]))
    b.is_centered = True
    b.frame_color = None
    return b

class IfWidget(VBox):
    def __init__(self, if_node):
        self.if_node = if_node

        if_label = TextEdit(lambda : 'if', color=(255,30,30))
        
        cond_part = HBox(List([if_label, widget_for(self.if_node.expr)]))
        cond_part.is_centered = True
        
        if_true_part = tabbed(widget_for(self.if_node.if_true))

        parts = [cond_part, widget_for('{'), if_true_part, widget_for('}')]
        if self.if_node.if_false:
            if_false_part = [widget_for('else {'), tabbed(widget_for(self.if_node.if_false)), widget_for('}')]
            parts.append(if_false_part)
            
        
        VBox.__init__(self, List(parts))
