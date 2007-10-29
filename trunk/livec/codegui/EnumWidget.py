# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.Box import VBox, HBox
from gui.TextEdit import TextEdit, make_label
from codegui.loop import loop
from codegui.widget_for import NormalWidgetMaker, indented
import style

from lib.observable.List import List

from functools import partial

class EnumWidget(VBox):
    # TODO: emphasize_value should be a proxy?
    def __init__(self, enum_proxy, emphasize_value=None):
        self.enum = enum_proxy.get()

        self._comma = make_label(style.comma, ',')
        values_box = VBox(List([
            self._value_widget(value_proxy, index!=len(self.enum.values)-1,
                               emphasize_value)
            for index, value_proxy in enumerate(self.enum.values)
        ]))

        VBox.__init__(self, List([
            HBox(List([
                make_label(style.enum, 'enum'),
                make_label(style.space, ' '),
                make_label(style.type_, loop.namer.get_name(self.enum)),
            ]), relay_focus=True),
            make_label(style.braces, '{'),
            indented(values_box),
            HBox(List([
                make_label(style.braces, '}'),
                make_label(style.semicolon, ';'),
            ]), relay_focus=True)
        ]))

    def _value_widget(self, value_proxy, with_comma, emphasize_value):
        value = value_proxy.get()
        s = style.enum_value
        if value is emphasize_value:
            s = style.emphasize(s)
        l = [
            TextEdit(s, partial(loop.namer.get_name, value)),
            make_label(style.operator, ' = '),
            NormalWidgetMaker.make(value.value),
        ]
        if with_comma:
            l.append(self._comma)
        return HBox(List(l))
