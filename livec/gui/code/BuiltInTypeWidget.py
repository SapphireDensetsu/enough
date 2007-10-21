from gui.Box import VBox
from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for

class BuiltInTypeWidget(VBox):
    def __init__(self, _type):
        self.type = _type
        self.meta_widget = widget_for(self.type.meta)
        self.name_widget = TextEdit(lambda : self.type.name)
        VBox.__init__(self, lambda : [self.meta_widget, self.name_widget])
