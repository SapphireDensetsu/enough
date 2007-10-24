from gui.Box import HBox
from gui.TextEdit import make_label
from gui.loop import loop
from gui.code.widget_for import widget_for, indented
import style

from lib.observable.List import List

class DefineWidget(HBox):
    def __init__(self, define):
        self.define = define

        HBox.__init__(self, List([
            make_label(style.define, '#define'),
            make_label(style.space, ' '),
            make_label(style.define_value, loop.namer.get_name(self.define)),
            make_label(style.space, ' '),
            widget_for(self.define.expr),
        ]), relay_focus=True)
