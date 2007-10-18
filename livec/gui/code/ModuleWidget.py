from gui.VBox import VBox
#from gui.Label import Label
from gui.code import widget_for

class ModuleWidget(VBox):
    def __init__(self, module):
        self.module = module
        VBox.__init__(self, self.get_children)
    def get_children(self):
        yield widget_for(self.module.meta)
