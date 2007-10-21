from gui.Box import VBox
from gui.TextEdit import TextEdit
from gui.code import widget_for
from CacheMap import CacheMap
from List import List

class ModuleWidget(VBox):
    def __init__(self, module):
        self.module = module
        ibox = VBox(CacheMap(widget_for, self.module.functions))
        VBox.__init__(self, List([
            TextEdit(lambda : self.module.meta['name']),
            ibox,
        ]))
