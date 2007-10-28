from gui.TextEdit import TextEdit
import style

class StatementFillerWidget(TextEdit):
    def __init__(self, filler_proxy):
        TextEdit.__init__(self, style.filler, self._get_text)
        self.filler_proxy = filler_proxy
        self.selectable.set(True)

    def _get_text(self):
#        if not self._text:
            return '<statement filler>'
