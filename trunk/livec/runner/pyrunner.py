import nodewalker
import nodes

import pybuiltins

class PyRunner(object):
    def __init__(self, module):
        self.module = module
        imports = nodewalker.imports(module)

        pytypes = {LiteralInt: pybuiltins,
                   LiteralString: str,
                   LiteralChar: CChar
        
    def run_func(self, func, args):
        
