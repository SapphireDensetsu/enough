from gui.Box import VBox, HBox
from gui.code.widget_for import widget_for, ccode_widget_for
from gui.TextEdit import make_label
from gui.code import style

from observable.List import List

from itertools import chain

class BinaryOpWidget(HBox):
    op_string = None
    operand_attrs = 'a', 'b'
    def __init__(self, node):
        self.node = node

        HBox.__init__(self, List([
            widget_for(getattr(self.node, self.operand_attrs[0])),
            make_label(' ' + self.op_string + ' ', color=style.paren_color),
            widget_for(getattr(self.node, self.operand_attrs[1])),
        ]))
        self.is_centered = True
        

class EqualsWidget(BinaryOpWidget):
    op_string = '=='

class NotEqualsWidget(BinaryOpWidget):
    op_string = '!='

class AssignWidget(BinaryOpWidget):
    op_string = '='
    operand_attrs = 'lvalue', 'rvalue'

class SubtractWidget(BinaryOpWidget):
    op_string = '-'
    operand_attrs = 'lexpr', 'rexpr'
