from styletools import StyledTextEdit

class IdentifierWidget(StyledTextEdit):
    def __init__(self, variable, color):
        self.variable = variable
        name = self.variable.meta.get('name', '<noname>')
        StyledTextEdit.__init__(self, (lambda : name), color=color)
