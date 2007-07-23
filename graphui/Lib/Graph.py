class HasCyclesError(Exception): pass
class NodeWasntConnected(Exception): pass

class Node(object):
    def __init__(self, value):
        self.value = value
        self.connections = {'in': [], 'out': []}

    def connect_out(self, other):
        self.connections['out'].append(other)
        other.connections['in'].append(self)

    def connect_in(self, other):
        other.connections['out'].append(self)
        self.connections['in'].append(other)

    def disconnect(self, other):
        was_connected=False
        if other in self.connections['out'][:]:
            other.connections['in'].remove(self)
            self.connections['out'].remove(other)
            was_connected=True
        if other in self.connections['in'][:]:
            other.connections['out'].remove(self)
            self.connections['in'].remove(other)
            was_connected=True

        if not was_connected:
            raise NodeWasntConnected(other)

    def disconnect_all(self):
        for other in self.connections['out'][:]:
            other.connections['in'].remove(self)
            self.connections['out'].remove(other)
        for other in self.connections['in'][:]:
            other.connections['out'].remove(self)
            self.connections['in'].remove(other)
            
    def is_connected(self, other):
        if ((other in self.connections['out'])
            or (other in self.connections['in'])):
            return True
        return False
        
    def __repr__(self):
        return '<%s: value=%r, out=%r, in=%r>' % (self.__class__.__name__, self.value, len(self.connections['out']), len(self.connections['in']))

    def number_of_outgoing_offspring(self):
        # todo this is unoptimal
        # Only works for tree, not for full graphs with cycles
        offspring = list(self.connections['out'])
        i = 0
        while i < len(offspring):
            child = offspring[i]
            for subchild in child.connections['out']:
                if subchild in offspring:
                    raise HasCyclesError()
                offspring.append(subchild)
            i += 1
        return len(offspring)


    def iter_all_connections(self):
        for other in self.connections['out']:
            yield other
        for other in self.connections['in']:
            yield other
            
        
def copy(orig_nodes):
    nodes = []
    nodes_map = {}
    nodes_reverse_map = {}
    for node in orig_nodes:
        new = Node(node.value)
        for con_type, others in node.connections.iteritems():
            new.connections[con_type] = others[:]
        nodes.append(new)
        nodes_map[node] = new
        nodes_reverse_map[new] = node

    for node in nodes:
        for con_type, others in node.connections.iteritems():
            for i in xrange(len(others)):
                others[i] = nodes_map[others[i]]
        
    return nodes, nodes_map, nodes_reverse_map
        
def topological_sort(orig_nodes):
    out = []
    cur = []

    nodes, nodes_map, nodes_reverse_map = copy(orig_nodes)
    
    for node in nodes:
        if not node.connections['in']:
            cur.append((0, node))

    while cur:
        level, node = cur.pop(0)
        out.append((level, node))
        out_nodes = node.connections['out'][:]
        for out_node in out_nodes:
            node.disconnect(out_node)
            if not out_node.connections['in']:
                cur.append((level+1, out_node))

    for node in nodes:
        if node.connections['out'] or node.connections['in']:
            raise HasCyclesError(nodes)

    out = [(level, nodes_reverse_map[node]) for level, node in sorted(out)]
    return out

def generate_dot(nodes, graph_params=None):
    # Generates a DOT language description of the graph
    out = 'digraph G {\n'
    if graph_params is not None:
        out += 'graph ['
        for k,v in graph_params.iteritems():
            out+='%s=%s,' % (k,v)
        out += '];\n'
    for node in nodes:
        for other in node.connections['out']:
            out += '%s -> %s;\n' % (id(node), id(other))
        #for other in node.connections['in']:
        #    out += '%s -> %s;\n' % (id(other), id(node))
    return out + '}\n'

# This uses DOT to find the position of nodes in a graph
def get_drawing_data(dot, nodes):
    # TODO Fix bug when no nodes connected in graph!!
    d = generate_dot(nodes) # This should help but has no effect..., dict(splines='"polyline"'))
    g, n, e = dot.get_graph_data(d)
    out_nodes = {}
    out_edges = {}
    ids_to_nodes = {}
    for node in nodes:
        sid = str(id(node))
        ids_to_nodes[sid] = node
        if sid in n:
            out_nodes[node] = n[sid]
        if sid in e:
            out_edges[node] = e[sid]
    for out_node, edges in out_edges.iteritems():
        for edge in edges:
            edge['tail_node'] = ids_to_nodes[edge['tail']]
    return g, out_nodes, out_edges
