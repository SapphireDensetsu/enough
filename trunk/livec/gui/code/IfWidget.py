from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for, indented
from gui.code import style

from List import List

from itertools import chain


class IfWidget(VBox):
    def __init__(self, if_node):
        self.if_node = if_node

        cond_part = HBox(List([
            make_label('if', color=style.if_color),
            widget_for(self.if_node.expr),
        ]))
        cond_part.is_centered = True
        
        parts = [
            cond_part,
            make_label('{', color=style.braces_color),
            indented(widget_for(self.if_node.if_true)),
            make_label('}', color=style.braces_color),
        ]
        if self.if_node.if_false:
            if_false_part = [
                make_label('else', color=style.else_color),
                make_label('{', color=style.braces_color),
                indented(widget_for(self.if_node.if_false)),
                make_label('}', color=style.braces_color),
            ]
            parts.append(if_false_part)
            
        VBox.__init__(self, List(parts))
