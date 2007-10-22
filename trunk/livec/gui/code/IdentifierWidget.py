from gui.TextEdit import TextEdit

class IdentifierWidget(TextEdit):
    def __init__(self, variable, color):
        self.variable = variable
        name = self.variable.meta.get('name', '<noname>')
        TextEdit.__init__(self, (lambda : name), color=color)
