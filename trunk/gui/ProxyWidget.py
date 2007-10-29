# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from Widget import Widget

class ProxyWidget(Widget):
    """A widget that contains a proxy value widget that can change its
    value."""
    def __init__(self, value_proxy):
        Widget.__init__(self)
        self.value_proxy = value_proxy
        self.value_proxy.obs_value.add_observer(self, '_value_')
        self._update_proxy()

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.value_proxy)

    def draw(self, surface, pos):
        self.value_proxy.get().draw(surface, pos)
    
    def update(self):
        cw = self.value_proxy.get()
        cw.update()
        self.size = cw.size

    def _value_changed(self, old_value, new_value):
        old_value.selectable.obs_value.remove_observer(self)
        self._update_proxy()

    def _update_proxy(self):
        widget = self.value_proxy.get()
        widget.selectable.obs_value.add_observer(self, '_selectable_')
        self._proxy_to(self.value_proxy.get())
    
    def _proxy_to(self, widget):
        self.selectable.set(widget.selectable.get())
        self.keymap.set_next_keymap(widget.keymap)

    def _selectable_changed(self, old_value, new_value):
        self.selectable.set(new_value)
