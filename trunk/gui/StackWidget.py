# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import pygame
from ProxyWidget import ProxyWidget
from SpacerWidget import SpacerWidget
from lib.observable.ValueContainer import ValueContainer

class StackWidget(ProxyWidget):
    _spacer = SpacerWidget((0, 0))
    def __init__(self):
        ProxyWidget.__init__(self, ValueContainer(self._spacer))
        self.items = []
    def push(self, widget):
        self.items.append(widget)
        self._update_state()
    def remove(self, item):
        self.items.remove(item)
        self._update_state()
    def pop(self):
        self.items.pop()
        self._update_state()
    def top(self):
        if not self.items:
            return None
        return self.items[-1]
    def _update_state(self):
        top = self.top()
        if top is not None:
            self.value_proxy.set(top)
        else:
            self.value_proxy.set(_spacer)
