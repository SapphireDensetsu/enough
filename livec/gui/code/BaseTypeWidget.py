from gui.TextEdit import TextEdit
from gui.code.widget_for import widget_for

class BaseTypeWidget(TextEdit):
    def __init__(self, _type):
        self.type = _type
        TextEdit.__init__(self, lambda : self.type.name, color=(0, 255, 0))
