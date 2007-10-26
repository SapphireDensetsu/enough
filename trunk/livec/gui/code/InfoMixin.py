# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.loop import loop

class InfoMixin(object):
    def got_focus(self):
        super(InfoMixin, self).got_focus()
        loop.browser.add_info_widget(self._info_widget)
    def lost_focus(self):
        super(InfoMixin, self).lost_focus()
        loop.browser.remove_info_widget(self._info_widget)
