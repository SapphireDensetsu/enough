import nodes
import itertools
import functools

def visit_all(x, visited=None):
    if visited is None:
        visited = set()
    visited.add(x)
    yield x
    for i in x.referred():
        if i in visited:
            continue
        for x in visit_all(i, visited):
            yield x

def concat_lines(func):
    @functools.wraps(func)
    def new_func(*args, **kw):
        return '\n'.join(func(*args, **kw)) + '\n'
    return new_func

class CCodeGenerator(object):
    def __init__(self):
        self._cnames = {}
        self._names = self._make_names()

    def _make_names(self):
        for i in itertools.count():
            yield 'name%d' % (i,)

    def _cname(self, node):
        if node not in self._cnames:
            if 'name' in node.meta:
                name = node.meta['name']
            else:
                name = '_'.join((node.__class__.__name__, self._names.next()))
            self._cnames[node] = name
        return self._cnames[node]
        
    def _cbasetype(self, node):
        if isinstance(node, nodes.BuiltinType):
            return node.name
        elif isinstance(node, nodes.Ptr):
            return self._cbasetype(node.pointed_type)

    def _cposttype(self, node, name):
        if isinstance(node, nodes.BuiltinType):
            return name
        elif isinstance(node, nodes.Ptr):
            return '(*%s)' % (self._cposttype(node.pointed_type, name),)

    def ctypedeclcode(self, node, name):
        return '%s %s' % (self._cbasetype(node), self._cposttype(node, name))

    def cdeclcode(self, node):
        if isinstance(node, nodes.Function):
            return self._Function_cdeclcode(node)
        elif isinstance(node, nodes.Enum):
            return 'enum %s {%s};' % (
                self._cname(node),
                ', '.join('%s=%s' % (self._cname(value), self.ccode(value.value))
                          for value in node.values))
        elif isinstance(node, nodes.Variable):
            return self.ctypedeclcode(node.type, self._cname(node))
        elif isinstance(node, nodes.Define):
            return '#define %s %s' % (self._cname(node), self.ccode(node.expr))

    @concat_lines
    def _Function_cdeclcode(self, node):
        yield '%s(%s)' % (self.ctypedeclcode(node.return_type, self._cname(node)),
                          ', '.join(self.ccode(param)
                                    for param in node.parameters))
        yield '{'
        yield self.ccode(node.block)
        yield '}'


    def ccode(self, node):
        if isinstance(node, nodes.Call):
            return '(%s(%s))' % (self.ccode(node.func),
                                 ','.join(self.ccode(arg)
                                          for arg in node.args))
        elif isinstance(node, nodes.Assign):
            return '(%s=%s)' % (self.ccode(node.lvalue), self.ccode(node.rvalue))
        elif isinstance(node, nodes.Declaration):
            return self.cdeclcode(node.obj)
        elif isinstance(node, nodes.Variable):
            return self._cname(node)
        elif isinstance(node, nodes.Define):
            return self._cname(node)
        elif isinstance(node, nodes.EnumValue):
            return self._cname(node)
        elif isinstance(node, nodes.Import):
            return node.name
        elif isinstance(node, nodes.ArrayDeref):
            return '(%s[%s])' % (self.ccode(node.expr), self.ccode(node.index))
        elif isinstance(node, nodes.Subtract):
            return '(%s-%s)' % (self.ccode(node.lexpr), self.ccode(node.rexpr))
        elif isinstance(node, nodes.LiteralInt):
            return str(node.value)
        elif isinstance(node, nodes.LiteralString):
            return '"%s"' % node._c_escape(node.value,)
        elif isinstance(node, nodes.LiteralChar):
            return "'%c'" % (node.value,)
        elif isinstance(node, nodes.NotEquals):
            return '(%s!=%s)' % (self.ccode(node.a), self.ccode(node.b))
        elif isinstance(node, nodes.Equals):
            return '(%s==%s)' % (self.ccode(node.a), self.ccode(node.b))
        elif isinstance(node, nodes.Return):
            return 'return %s' % (self.ccode(node.expr),)
        elif isinstance(node, nodes.Module):
            return self._Module_ccode(node)
        elif isinstance(node, nodes.Block):
            return self._Block_ccode(node)
        elif isinstance(node, nodes.If):
            return self._If_ccode(node)

    @concat_lines
    def _Module_ccode(self, node):
        for x in self._includes(node):
            yield '#include %s' % (x,)
        for x in node.defines:
            yield self.ccode(x)
        for x in node.types:
            yield self.ccode(x) + ';'
        for x in node.variable_declarations:
            yield self.ccode(x) + ';'
        for x in node.functions:
            yield self.ccode(x)

    @concat_lines
    def _Block_ccode(self, node):
        yield '{'
        for variable_declaration in node.variable_declarations:
            yield self.ccode(variable_declaration) + ';'
        for statement in node.statements:
            yield self.ccode(statement) + ';'
        yield '}'

    @concat_lines
    def _If_ccode(self, node):
        yield 'if(%s)' % (self.ccode(node.expr),)
        yield '{'
        yield self.ccode(node.if_true)
        yield '}'
        if node.if_false is not None:
            yield 'else'
            yield '{'
            yield self.ccode(node.if_false)
            yield '}'

    def _includes(self, node):
        i = set()
        for x in visit_all(node):
            if isinstance(x, nodes.Import):
                i.add(x.include)
        return i
