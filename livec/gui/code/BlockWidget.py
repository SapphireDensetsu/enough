from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
from gui.code.widget_for import widget_for, ccode_widget_for

from List import List

class BlockWidget(VBox):
    def __init__(self, block):
        self.block = block
        VBox.__init__(self, List(map(widget_for, self.block.statements)))
