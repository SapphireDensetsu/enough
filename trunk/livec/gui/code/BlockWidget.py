from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for, ccode_widget_for

from CacheMap import CacheMap
from List import List

class BlockWidget(VBox):
    def __init__(self, block):
        self.block = block
        VBox.__init__(self, CacheMap(widget_for, List(self.block.statements)))
