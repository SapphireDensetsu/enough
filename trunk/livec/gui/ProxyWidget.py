# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from Widget import Widget
from Spacer import Spacer
from lib.observable.ValueProxy import ValueProxy

class ProxyWidget(Widget):
    """A widget that contains a proxy value widget that can change its
    value."""
    _spacer = Spacer((0, 0))
    def __init__(self, value_proxy=None):
        Widget.__init__(self)
        if value_proxy is None:
            value_proxy = ValueProxy()
        self._value_proxy = value_proxy
        self._value_proxy.obs_value.add_observer(self, '_value_')
        self._update_proxy()

    def draw(self, surface, pos):
        self._current_widget().draw(surface, pos)
    
    def update(self):
        cw = self._current_widget()
        cw.update()
        self.size = cw.size

    def _value_changed(self, old_value, new_value):
        self._update_proxy()

    def _value_added(self, new_value):
        self._update_proxy()

    def _value_deleted(self, old_value):
        self._update_proxy()

    def _update_proxy(self):
        self._proxy_to(self._current_widget())
    
    def _current_widget(self):
        if self._value_proxy.exists():
            return self._value_proxy.get()
        else:
            return self._spacer

    def _proxy_to(self, widget):
        self.selectable = widget.selectable
        self.keymap.set_next_keymap(widget.keymap)
