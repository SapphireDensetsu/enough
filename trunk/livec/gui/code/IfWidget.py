from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for, indented
from gui.code import style

from observable.List import List

from itertools import chain


class IfWidget(VBox):
    def __init__(self, if_node):
        self.if_node = if_node

        cond_part = HBox(List([
            make_label(style.if_, 'if'),
            make_label(style.paren, '('),
            widget_for(self.if_node.expr),
            make_label(style.paren, ')'),
        ]))
        cond_part.is_centered = True
        
        parts = [
            cond_part,
            make_label(style.braces, '{'),
            indented(widget_for(self.if_node.if_true)),
            make_label(style.braces, '}'),
        ]
        if self.if_node.if_false:
            if_false_part = [
                make_label(style.else_, 'else'),
                make_label(style.braces, '{'),
                indented(widget_for(self.if_node.if_false)),
                make_label(style.braces, '}'),
            ]
            parts.append(if_false_part)
            
        VBox.__init__(self, List(parts))
