from gui.Box import VBox, HBox
from styletools import styled_label
from gui.code.widget_for import widget_for, indented
from gui.code import style

from observable.List import List

from itertools import chain


class IfWidget(VBox):
    def __init__(self, if_node):
        self.if_node = if_node

        cond_part = HBox(List([
            styled_label('if', color=style.if_color),
            styled_label('(', color=style.paren_color),
            widget_for(self.if_node.expr),
            styled_label(')', color=style.paren_color),
        ]))
        cond_part.is_centered = True
        
        parts = [
            cond_part,
            styled_label('{', color=style.braces_color),
            indented(widget_for(self.if_node.if_true)),
            styled_label('}', color=style.braces_color),
        ]
        if self.if_node.if_false:
            if_false_part = [
                styled_label('else', color=style.else_color),
                styled_label('{', color=style.braces_color),
                indented(widget_for(self.if_node.if_false)),
                styled_label('}', color=style.braces_color),
            ]
            parts.append(if_false_part)
            
        VBox.__init__(self, List(parts))
