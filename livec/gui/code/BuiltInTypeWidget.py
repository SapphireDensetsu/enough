from gui.TextEdit import TextEdit
from gui.code.widget_for import widget_for

from List import List

# TODO: This is actually any named type, builtin or typedef, and can
# even accomodate struct names/etc.
class BuiltInTypeWidget(TextEdit):
    def __init__(self, _type):
        self.type = _type
        TextEdit.__init__(self, lambda : self.type.name, color=(0, 255, 0))
