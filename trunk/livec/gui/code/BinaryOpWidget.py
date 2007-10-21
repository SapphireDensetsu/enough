from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for, ccode_widget_for

from CacheMap import CacheMap
from List import List

from itertools import chain

class BinaryOpWidget(HBox):
    op_char = None
    operand_attrs = 'a', 'b'
    def __init__(self, node):
        self.node = node

        HBox.__init__(self, CacheMap(widget_for, List(['(',
                                                       getattr(self.node, self.operand_attrs[0]),
                                                       self.op_char,
                                                       getattr(self.node, self.operand_attrs[1]),
                                                       ')',])
                                                ))
        self.is_centered = True
        

class EqualsWidget(BinaryOpWidget):
    op_char = '=='

class NotEqualsWidget(BinaryOpWidget):
    op_char = '!='

class AssignWidget(BinaryOpWidget):
    op_char = '='
    operand_attrs = 'lvalue', 'rvalue'

class SubtractWidget(BinaryOpWidget):
    op_char = '-'
    operand_attrs = 'lexpr', 'rexpr'
