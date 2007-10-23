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


class NodeWalker(object):
    def _find_all(self, node, predicat):
        # TODO: node must be root. If its not root, then this should
        # not walk the referred() graph but children() (that does not
        # yet exist).
        i = set()
        for x in visit_all(node):
            if predicat(x):
                i.add(x)
        return i

    def _find_type(self, node, typ):
        def p(x):
            return isinstance(x, typ)
        return self._find_all(node, p)

    def _imports(self, node):
        return self._find_type(node, nodes.Import)

    def _includes(self, node):
        return set(imp.include for imp in self._imports(node))

    def _defines(self, node):
        return self._find_type(node, nodes.Define)

    def _variables(self, node):
        return self._find_type(node, nodes.Variable)

    def _types(self, node):
        return self._find_type(node, nodes.Enum)

    
