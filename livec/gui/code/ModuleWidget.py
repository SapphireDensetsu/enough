from gui.Box import VBox
#from gui.Label import Label
from gui.code import widget_for

class ModuleWidget(VBox):
    def __init__(self, module):
        self.module = module
        self.meta_widget = widget_for(self.module.meta)
        self.function_widgets = [widget_for(func) for func in self.module.functions]
        VBox.__init__(self)
        self.add_child(self.meta_widget)
        for func_widget in self.function_widgets:
            self.add_child(func_widget)
