# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

'''
Generates C text code from a model tree of nodes.

The CCodeGenerator is a class (has state) because while traversing the tree, we need to remember
what symbols the current scope contains (which variables are defined, etc.).


Every method of CCodeGenerator that produces code, is a generator of lines of text.
The usability method .ccode takes all these lines and joins them to a single string.

To recursively find types, imports, defines, in the tree we use nodewalker. functions.

Before entering any code block, we set the current "scope" by changing the set of declaration that
matches that code block. This is done using the _declared context method:

Example from function code generation:

        with self._declared(node.type.parameters):
            for line in self._ccode(node.block):
                yield line
'''

from __future__ import with_statement
import nodes
import itertools
import functools
import contextlib

import nodewalker

def concat_lines(func):
    @functools.wraps(func)
    def new_func(*args, **kw):
        return '\n'.join(func(*args, **kw)) + '\n'
    return new_func

def is_expr(node):
    return isinstance(node, (nodes.Call,
                             nodes.Assign,
                             nodes.Variable,
                             nodes.Define,
                             nodes.EnumValue,
                             nodes.Import,
                             nodes.ArrayDeref,
                             nodes.Subtract,
                             nodes.LiteralInt,
                             nodes.LiteralString,
                             nodes.LiteralChar,
                             nodes.NotEquals,
                             nodes.Equals))

class CCodeGenerator(object):
    def __init__(self):
        self._cnames = {}
        self._names = self._make_names()
        self._decls = set()

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
        elif isinstance(node, nodes.FunctionType):
            return self._cbasetype(node.return_type)
        else:
            assert False, "Cannot find base type of %r" % (node,)

    def _cposttype(self, node, name):
        if isinstance(node, nodes.BuiltinType):
            return name
        elif isinstance(node, nodes.Ptr):
            return '(*%s)' % (self._cposttype(node.pointed_type, name),)
        elif isinstance(node, nodes.FunctionType):
            return '%s(%s)' % (self._cposttype(node.return_type, name),
                               ', '.join(self.vardeclcode(param)
                                         for param in node.parameters))
        else:
            assert False, "Cannot find post type of %r" % (node,)

    def ctypedeclcode(self, node, name):
        return '%s %s' % (self._cbasetype(node), self._cposttype(node, name))

    def cdeclcode(self, node):
        if isinstance(node, nodes.Function):
            return self._Function_cdeclcode(node)
        elif isinstance(node, nodes.Enum):
            return self._Enum_cdeclcode(node)
        elif isinstance(node, nodes.Define):
            return self._Define_cdeclcode(node)
        elif isinstance(node, nodes.Variable):
            return [self.vardeclcode(node) + ';']
        else:
            assert False, "No declcode for %r" % (node,)

    def vardeclcode(self, node):
        assert isinstance(node, nodes.Variable)
        return self.ctypedeclcode(node.type, self._cname(node))

    def _Define_cdeclcode(self, node):
        yield '#define %s (%s)' % (self._cname(node), self._exprcode(node.expr))

    def _Enum_cdeclcode(self, node):
        yield 'enum %s' % (self._cname(node),)
        yield '{'
        for value in node.values[:-1]:
            yield '    %s=%s,' % (self._cname(value), self._exprcode(value.value))
        value = node.values[-1]
        yield '    %s=%s' % (self._cname(value), self._exprcode(value.value))
        yield '};'


    def _Function_cdeclcode(self, node):
        yield self.ctypedeclcode(node.type, self._cname(node))
        with self._declared(node.type.parameters):
            for line in self._ccode(node.block):
                yield line

    def _declare(self, decls):
        l = len(self._decls)
        self._decls |= set(decls)
        assert len(self._decls) == l + len(decls)

    def _undeclare(self, decls):
        self._decls -= set(decls)

    def _is_declared(self, decl):
        return decl in self._decls

    @contextlib.contextmanager
    def _declared(self, decls):
        """With the given declarations as declared"""
        self._declare(decls)
        try:
            yield
        finally:
            self._undeclare(decls)

    @concat_lines
    def ccode(self, node):
        return self._ccode(node)

    def _ccode(self, node):
        if isinstance(node, nodes.Declaration):
            return self.cdeclcode(node.obj)
        elif isinstance(node, nodes.Module):
            return self._Module_ccode(node)
        elif isinstance(node, nodes.Block):
            return self._Block_ccode(node)
        elif isinstance(node, nodes.If):
            return self._If_ccode(node)
        elif isinstance(node, nodes.Return):
            return ['return %s;' % (self._exprcode(node.expr),)]
        return [self._exprcode(node) + ';']
    
    def _exprcode(self, node):
        if isinstance(node, nodes.Call):
            return '(%s(%s))' % (self._exprcode(node.func),
                                 ','.join(self._exprcode(arg)
                                          for arg in node.args))
        elif isinstance(node, nodes.Assign):
            return '(%s=%s)' % (self._exprcode(node.lvalue), self._exprcode(node.rvalue))
        elif isinstance(node, nodes.Variable):
            return self._cname(node)
        elif isinstance(node, nodes.Define):
            return self._cname(node)
        elif isinstance(node, nodes.EnumValue):
            return self._cname(node)
        elif isinstance(node, nodes.Import):
            return node.name
        elif isinstance(node, nodes.ArrayDeref):
            return '(%s[%s])' % (self._exprcode(node.expr), self._exprcode(node.index))
        elif isinstance(node, nodes.Subtract):
            return '(%s-%s)' % (self._exprcode(node.lexpr), self._exprcode(node.rexpr))
        elif isinstance(node, nodes.LiteralInt):
            return str(node.value)
        elif isinstance(node, nodes.LiteralString):
            return '"%s"' % self._cescape(node.value,)
        elif isinstance(node, nodes.LiteralChar):
            return "'%c'" % (node.value,)
        elif isinstance(node, nodes.NotEquals):
            return '(%s!=%s)' % (self._exprcode(node.a), self._exprcode(node.b))
        elif isinstance(node, nodes.Equals):
            return '(%s==%s)' % (self._exprcode(node.a), self._exprcode(node.b))
        else:
            assert False, "Don't know how to make ccode for %r" % (node,)

    def _cescape(self, value):
        return value.replace('\\', '\\\\').replace('\n', '\\n')

    def _Module_ccode(self, node):
        for x in nodewalker.includes(node):
            yield '#include %s' % (x,)
        defs = list(nodewalker.defines(node))
        for x in defs:
            for line in self.cdeclcode(x):
                yield line
        with self._declared(defs):
            types = list(nodewalker.types(node))
            for x in types:
                for line in self.cdeclcode(x):
                    yield line
            with self._declared(types):
                for x in node.variables:
                    if self._is_declared(x):
                        continue
                    for line in self.cdeclcode(x):
                        yield line
                with self._declared(node.variables):
                    for x in node.functions:
                        for line in self.cdeclcode(x):
                            yield line

    def _Block_ccode(self, node):
        yield '{'
        for var in nodewalker.variables(node):
            if self._is_declared(var):
                continue
            for line in self.cdeclcode(var):
                yield '    ' + line
        for statement in node.statements:
            for line in self._ccode(statement):
                yield '    ' + line
        yield '}'

    def _indented_ccode(self, node):
        ccode_lines = self._ccode(node)
        if isinstance(node, nodes.Block):
            for line in ccode_lines:
                yield line
        else:
            for line in ccode_lines:
                yield '    ' + line

    def _If_ccode(self, node):
        yield 'if(%s)' % (self._exprcode(node.expr),)
        for line in self._indented_ccode(node.if_true):
            yield line
        if node.if_false is not None:
            yield 'else'
            for line in self._indented_ccode(node.if_false):
                yield line

c_escape_common = {
    '\\' : '\\\\',
    '\t' : '\\t',
    '\r' : '\\r',
    '\n' : '\\n',
}

c_escape_char = c_escape_common.copy()
c_escape_char["'"] = "\\'"

c_escape_str = c_escape_common.copy()
c_escape_str['"'] = '\\"'
