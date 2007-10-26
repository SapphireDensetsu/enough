# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

import nodes

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


def find_all(node, predicat):
    # TODO: node must be root. If its not root, then this should
    # not walk the referred() graph but children() (that does not
    # yet exist).
    i = set()
    for x in visit_all(node):
        if predicat(x):
            i.add(x)
    return i

def find_type(node, typ):
    def p(x):
        return isinstance(x, typ)
    return find_all(node, p)

def imports(node):
    return find_type(node, nodes.Import)

def includes(node):
    return set(imp.include for imp in imports(node))

def defines(node):
    return find_type(node, nodes.Define)

def variables(node):
    return find_type(node, nodes.Variable)

def types(node):
    return find_type(node, nodes.Enum)
