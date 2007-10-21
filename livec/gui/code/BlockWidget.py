from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for, ccode_widget_for


class BlockWidget(VBox):
    def __init__(self, block):
        self.block = block
        self.meta_widget = widget_for(self.block.meta)
        self.statements_Widgets = [ccode_widget_for(s) for s in self.block.statements]
        VBox.__init__(self)
        self.add_child(self.meta_widget)
        for stmt in self.statements_Widgets:
            self.add_child(stmt)
