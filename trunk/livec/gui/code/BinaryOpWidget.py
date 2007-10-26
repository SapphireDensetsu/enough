# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from gui.code.widget_for import widget_for, ccode_widget_for
from gui.TextEdit import make_label
from gui.code import style
from gui.ProxyWidget import ProxyWidget

from lib.observable.List import List
from lib.observable.DictOfAttrs import DictOfAttrs
from lib.DictMap import DictMap

from itertools import chain

class BinaryOpWidget(HBox):
    op_string = None
    def __init__(self, node):
        self.node = node

        d = DictMap(DictOfAttrs(self.node))

        left, right = self.operand_attrs
        HBox.__init__(self, List([
            ProxyWidget(d.map(left, widget_for)),
            make_label(style.operator, ' ' + self.op_string + ' '),
            ProxyWidget(d.map(right, widget_for)),
        ]))
        self.is_centered = True
        

class EqualsWidget(BinaryOpWidget):
    op_string = '=='
    operand_attrs = 'a', 'b'

class NotEqualsWidget(BinaryOpWidget):
    op_string = '!='
    operand_attrs = 'a', 'b'

class AssignWidget(BinaryOpWidget):
    op_string = '='
    operand_attrs = 'lvalue', 'rvalue'

class SubtractWidget(BinaryOpWidget):
    op_string = '-'
    operand_attrs = 'lexpr', 'rexpr'
