from gui.TextEdit import TextEdit
from gui.Box import HBox
#from gui.Label import Label
from gui.code import widget_for

from CacheMap import CacheMap
from List import List

class PtrTypeWidget(HBox):
    def __init__(self, _type):
        self.type = _type
        HBox.__init__(self, CacheMap(widget_for, List(['*', self.type.pointed_type])))
        self.is_centered = True
