from gui.TextEdit import TextEdit

class IdentifierWidget(TextEdit):
    def __init__(self, variable, style):
        self.variable = variable
        name = self.variable.meta.get('name', '<noname>')
        TextEdit.__init__(self, style, (lambda : name))
