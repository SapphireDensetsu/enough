## /* Copyright 2007, Noam Lewis, enoughmail@googlegroups.com */
## /*
##     This file is part of Enough.

##     Enough is free software; you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation; either version 3 of the License, or
##     (at your option) any later version.

##     Enough is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>.
## */

# Generic graph module

class HasCyclesError(Exception): pass
class NodeWasntConnected(Exception): pass

class Node(object):
    def __init__(self, value):
        self.value = value
        self.connections = {'in': [], 'out': []}

    def connect(self, other):
        self.connections['out'].append(other)
        other.connections['in'].append(self)

    def disconnect(self, other):
        if other not in self.connections['out']:
            raise NodeWasntConnected(other)
        self.connections['out'].remove(other)
        other.connections['in'].remove(self)

    def disconnect_all(self):
        for other in self.connections['out'][:]:
            other.connections['in'].remove(self)
            self.connections['out'].remove(other)
        for other in self.connections['in'][:]:
            other.connections['out'].remove(self)
            self.connections['in'].remove(other)
            
    def is_connected(self, other):
        return other in self.connections['out']
        
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

def generate_dot(groups, graph_params=None):
    # Generates a DOT language description of the graph
    out = 'digraph G {\n'
    if graph_params is not None:
        out += 'graph ['
        for k,v in graph_params.iteritems():
            out+='%s=%s,' % (k,v)
        out += '];\n'
    for group_name, nodes in groups.iteritems():
        out += 'subgraph "%s" {\n' % (group_name,)
        for node in nodes:
            
            props_str = ','.join('%s=%s,' % (prop_name, value)
                                 for prop_name, value in node.value.get_node_properties().iteritems())
                
            out += '%s [%s];\n' % (id(node), props_str)
            for other in node.connections['out']:
                out += '%s -> %s;\n' % (id(node), id(other))
                
        out += '}\n'
    return out + '}\n'

# This uses DOT to find the position of nodes in a graph
def get_drawing_data(dot, groups):
    data = generate_dot(groups)
    d = dot.get_graph_data(data)
    d.addCallback(_data_received, groups)
    return d

def _data_received((g, n, e), groups):
    out_nodes = {}
    out_edges = {}
    ids_to_nodes = {}
    for group_name, nodes in groups.iteritems():
        for node in nodes:
            sid = str(id(node))
            ids_to_nodes[sid] = node
            if sid in n:
                out_nodes[node] = n[sid]
            if sid in e:
                out_edges[node] = e[sid]
    for out_node, edges in out_edges.iteritems():
        for edge in edges:
            edge['head_node'] = ids_to_nodes[edge['head']]
    return g, out_nodes, out_edges
