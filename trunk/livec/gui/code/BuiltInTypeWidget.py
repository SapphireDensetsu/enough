from gui.TextEdit import TextEdit
#from gui.Label import Label
from gui.code import widget_for

from List import List

class BuiltInTypeWidget(TextEdit):
    def __init__(self, _type):
        self.type = _type
        TextEdit.__init__(self, lambda : self.type.name)
