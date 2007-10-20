from gui.Box import VBox
#from gui.Label import Label
from gui.code import widget_for

class ModuleWidget(VBox):
    def __init__(self, module):
        self.module = module
        self.meta_widget = widget_for(self.module.meta)
        self.function_widgets = [widget_for(func) for func in self.module.functions]
        VBox.__init__(self, lambda : [self.meta_widget] + self.function_widgets)
