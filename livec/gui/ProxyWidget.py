from Stack import Stack
from Spacer import Spacer

class ProxyWidget(Stack):
    """A widget that contains a proxy value widget that can change its
    value."""
    def __init__(self, proxy_value):
        Stack.__init__(self)
        self._spacer = Spacer((0, 0))
        proxy_value.obs_value.add_observer(self, '_value_')
        if proxy_value.exists():
            self.push(proxy_value.get())
        else:
            self.push(self._spacer)
    
    def _value_changed(self, old_value, new_value):
        assert old_value is self.pop()
        assert not self.items
        self.push(new_value)

    def _value_added(self, new_value):
        assert self._spacer is self.pop()
        assert not self.items
        self.push(new_value)

    def _value_deleted(self, old_value):
        assert old_value is self.pop()
        self.push(self._spacer)
