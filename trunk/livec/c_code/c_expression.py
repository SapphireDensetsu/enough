from base import CObject


import c_operators


class Expression(CObject):
    def __init__(self, op, args):
        self.op = op
        self.args = args
        self.meta = {}
    def __repr__(self):
        return '<%s op=%r, %d args>' % (self.__class__.__name__, self.op, len(self.args))
        
# The first arg in an expression is the operator or function,
# the rest are the arguments to the operator or function


def CodeBlock(expressions):
    return Expression(c_operators.SequentialExecution, expressions)


