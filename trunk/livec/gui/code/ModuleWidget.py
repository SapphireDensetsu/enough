from gui.Box import VBox
from gui.TextEdit import make_label
from gui.code.widget_for import widget_for, style
from observable.CacheMap import CacheMap
from observable.List import List

class ModuleWidget(VBox):
    def __init__(self, module):
        self.module = module
        ibox = VBox(CacheMap(widget_for, self.module.functions))
        ibox.frame_color = None
        VBox.__init__(self, List([
            make_label(self.module.meta['name'], color=style.module_name_color),
            ibox,
        ]))
