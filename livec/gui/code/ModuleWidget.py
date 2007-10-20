from gui.Box import VBox
#from gui.Label import Label
from gui.code import widget_for

class ModuleWidget(VBox):
    def __init__(self, module):
        self.module = module
        self.meta_widget = widget_for(self.module.meta)
        VBox.__init__(self, lambda : [self.meta_widget])
