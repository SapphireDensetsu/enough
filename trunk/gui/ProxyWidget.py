# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from Widget import Widget
from SpacerWidget import SpacerWidget
from lib.observable.ValueContainer import ValueContainer

class ProxyWidget(Widget):
    """A widget that contains a proxy value widget that can change its
    value."""
    _spacer = SpacerWidget((0, 0))
    def __init__(self, value_proxy=None):
        Widget.__init__(self)
        if value_proxy is None:
            value_proxy = ValueContainer()
        self.value_proxy = value_proxy
        self.value_proxy.obs_value.add_observer(self, '_value_')
        self._update_proxy()

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.value_proxy)

    def draw(self, surface, pos):
        self._current_widget().draw(surface, pos)
    
    def update(self):
        cw = self._current_widget()
        cw.update()
        self.size = cw.size

    def _value_changed(self, old_value, new_value):
        old_value.selectable.obs_value.remove_observer(self)
        self._update_proxy()

    def _value_added(self, new_value):
        self._update_proxy()

    def _value_deleted(self, old_value):
        old_value.selectable.obs_value.remove_observer(self)
        self._update_proxy()

    def _update_proxy(self):
        if self.value_proxy.exists():
            widget = self.value_proxy.get()
            widget.selectable.obs_value.add_observer(self, '_selectable_')
        self._proxy_to(self._current_widget())
    
    def _current_widget(self):
        if self.value_proxy.exists():
            return self.value_proxy.get()
        else:
            return self._spacer

    def _proxy_to(self, widget):
        self.selectable.set(widget.selectable.get())
        self.keymap.set_next_keymap(widget.keymap)

    def _selectable_changed(self, old_value, new_value):
        self.selectable.set(new_value)
