from Stack import Stack

class ProxyWidget(Stack):
    """A widget that contains a proxy value widget that can change its
    value."""
    def __init__(self, proxy_value):
        Stack.__init__(self)
        proxy_value.obs_value.add_observer(self, '_value_')
        if proxy_value.exists():
            self.push(proxy_value.get())
        else:
            assert False
    
    def _value_changed(self, old_value, new_value):
        assert old_value == self.pop()
        assert not self.items
        self.push(new_value)

    def _value_added(self, new_value):
        assert not self.items
        self.push(new_value)

    def _value_deleted(self, old_value):
        assert False
        assert old_value == self.pop()
