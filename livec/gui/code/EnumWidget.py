from gui.Box import VBox, HBox
from gui.TextEdit import make_label
from gui.loop import loop
from gui.code.widget_for import widget_for, indented
import style

from lib.observable.List import List

class EnumWidget(VBox):
    def __init__(self, enum, emphasize_value=None):
        self.enum = enum

        comma = make_label(style.comma, ',')
        def value_widget(value, with_comma):
            if value is emphasize_value:
                f = style.emphasize
            else:
                f = lambda x: x
            l = [
                make_label(f(style.enum_value), loop.namer.get_name(value)),
                make_label(f(style.operator), ' = '),
                widget_for(value.value),
            ]
            if with_comma:
                l.append(comma)
            return HBox(List(l))
        values_box = VBox(List([
            value_widget(value, index!=len(self.enum.values)-1)
            for index, value in enumerate(self.enum.values)
        ]))

        VBox.__init__(self, List([
            HBox(List([
                make_label(style.enum, 'enum'),
                make_label(style.space, ' '),
                make_label(style.type_, loop.namer.get_name(self.enum)),
            ]), relay_focus=True),
            make_label(style.braces, '{'),
            indented(values_box),
            make_label(style.braces, '}'),
        ]))
