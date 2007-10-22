from gui.TextEdit import TextEdit
from gui.code.widget_for import widget_for

import style

class BaseTypeWidget(TextEdit):
    def __init__(self, _type):
        self.type = _type
        TextEdit.__init__(style.base_type, self, lambda : self.type.name)
