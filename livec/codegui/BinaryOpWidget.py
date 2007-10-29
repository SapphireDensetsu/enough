# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from codegui.widget_for import NormalWidgetMaker
from gui.TextEdit import make_label
from codegui import style

from lib.observable.List import List

from itertools import chain

class BinaryOpWidget(HBox):
    op_string = None
    def __init__(self, node_proxy):
        self.node = node_proxy.get()

        left, right = self.operand_attrs
        HBox.__init__(self, List([
            NormalWidgetMaker.make(getattr(self.node, left)),
            make_label(style.operator, ' ' + self.op_string + ' '),
            NormalWidgetMaker.make(getattr(self.node, right)),
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
