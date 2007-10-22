from styletools import StyledTextEdit
from gui.code.widget_for import widget_for

class BaseTypeWidget(StyledTextEdit):
    def __init__(self, _type):
        self.type = _type
        StyledTextEdit.__init__(self, lambda : self.type.name, color = (0,255,0))
