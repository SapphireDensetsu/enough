# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.loop import loop

class InfoShower(object):
    def __init__(self, obs_activation):
        obs_activation.add_observer(self, '_focus_')
        self.info_widget = None
        self._added = None
    
    def _focus_activated(self):
        if self.info_widget is not None:
            loop.browser.add_info_widget(self.info_widget)
            self._added = self.info_widget
    
    def _focus_deactivated(self):
        if self._added is not None:
            loop.browser.remove_info_widget(self._added)
