## /* Copyright 2007, Eyal Lotem, Noam Lewis, enoughmail@googlegroups.com */
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

import observer

class HasCyclesError(Exception): pass
class NodeWasntConnected(Exception): pass
class EdgeWasntConnected(Exception): pass

class ObservableValue(object):
    def __init__(self, value):
        self._value = value
        self.obs = observer.Observable()
    def get_value(self):
        return self._value
    def set_value(self, value):
        self._value = value
        self.obj.notify.set_value(value)
    
class Edge(ObservableValue):
    def __init__(self, source, target, value):
        ObservableValue.__init__(self, value)
        self.source = source
        self.target = target
        self._value = value
        self.obs = observer.Observable()
        
        
class Node(ObservableValue):
    def __init__(self, value=None, inc=tuple(), outc=tuple()):
        ObservableValue.__init__(self, value)
        self.connections = {'in': list(inc), 'out': list(outc)}
        self.obs = observer.Observable()
    def __getstate__(self):
        return dict(value=self.value, connections=self.connections)

    def connect_node(self, other, edge_value=None):
        e = Edge(self, other, edge_value)
        self.connect_edge(e)
        return e

    def connect_edge(self, e):
        self.connections['out'].append(e)
        e.target.connections['in'].append(e)
        self.obs.notify.connect(e)

    def edges_connected_to(self, other):
        for e in self.connections['out']:
            if e.target == other:
                yield e
        
    def disconnect_node(self, other):
        edges = []
        for e in self.edges_connected_to(other):
            self.disconnect_edge(e)
            edges.append(e)
        return edges

    def disconnect_edge(self, edge):
        self.connections['out'].remove(edge)
        edge.target.connections['in'].remove(edge)
        self.obs.notify.disconnect(e)
        
    def disconnect_all(self):
        removed_edges = set()
        for e in self.connections['out'][:]:
            removed_edges.add(e)
            self.disconnect_edge(e)
        for e in self.connections['in'][:]:
            removed_edges.add(e)
            e.source.disconnect_edge(e)
        return removed_edges
            
    def is_connected_node(self, other):
        return other in (e.target for e in self.connections['out'])
        
    def is_connected_edge(self, edge):
        return edge in self.connections['out']
        
    def __repr__(self):
        return '<%s: value=%r, out=%r, in=%r>' % (self.__class__.__name__, self.value, len(self.connections['out']), len(self.connections['in']))

    def number_of_outgoing_offspring(self):
        # todo this is unoptimal
        # Only works for tree, not for full graphs with cycles
        offspring = [e.target for e in self.connections['out']]
        i = 0
        while i < len(offspring):
            child = offspring[i]
            for sub_edge in child.connections['out']:
                subchild = sub_edge.target
                if subchild in offspring:
                    raise HasCyclesError()
                offspring.append(subchild)
            i += 1
        return len(offspring)


    def iter_all_connections(self):
        for e in self.connections['out']:
            yield e
        for e in self.connections['in']:
            yield e
            
        
def copy(orig_nodes, node_value_copier=lambda x:x, edge_value_copier=lambda x:x):
    nodes = []
    nodes_map = {}
    nodes_reverse_map = {}
    for node in orig_nodes:
        new = Node(node_value_copier(node.value))
        for con_type, others in node.connections.iteritems():
            new.connections[con_type] = others[:]
        nodes.append(new)
        nodes_map[node] = new
        nodes_reverse_map[new] = node

    for node in nodes:
        for con_type, others in node.connections.iteritems():
            for i in xrange(len(others)):
                others[i] = Edge(node, nodes_map[others[i].target], edge_value_copier(others[i].value))
        
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
        out_nodes = [e.target for e in node.connections['out']]
        for out_node in out_nodes:
            node.disconnect_node(out_node)
            if not out_node.connections['in']:
                cur.append((level+1, out_node))

    for node in nodes:
        if node.connections['out'] or node.connections['in']:
            raise HasCyclesError(nodes)

    out = [(level, nodes_reverse_map[node]) for level, node in sorted(out)]
    return out


# ------------------------------------------------------------
# TODO move this to Dot.py?

def _repr_properties(props_dict):
    props_str = ','.join('%s=%s' % (prop_name, value)
                         for prop_name, value in props_dict.iteritems())
    return props_str


def generate_dot(groups, graph_params=None, edge_font_size=1):
    # Generates a DOT language description of the graph
    # Expects each node and edge instance, to have a .value.dot_properties() method
    out = 'digraph G {\n'
    out += 'graph [packMode=clust,'
    if graph_params is not None:
        for k,v in graph_params.iteritems():
            out+='%s=%s,' % (k,v)
    out += '];\n'
    for group_name, nodes in groups.iteritems():
        if group_name is not None:
            group_name = 'cluster_'+group_name
        else:
            group_name = 'no_cluster'
        out += 'subgraph %s {\n' % (group_name,)
        for node in nodes:
            props_str = ''#_repr_properties(node.value.dot_properties())
                
            out += '%s [%s];\n' % (id(node), props_str)
            for edge in node.connections['out']:
                other = edge.target
                edge_props = {}#edge.value.dot_properties()
                # OVERRIDE the real label with the id(edge), so we can
                # later correlate in dot's plain output which edge is
                # which.
                edge_props['label'] = id(edge)
                edge_props['fontsize'] = 3
                
                out += '%s -> %s [%s];\n' % (id(node), id(other), _repr_properties(edge_props))
                
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
    ids_to_edges = {}
    for group_name, nodes in groups.iteritems():
        for node in nodes:
            sid = str(id(node))

            assert sid not in ids_to_edges
            assert sid not in ids_to_nodes
            ids_to_nodes[sid] = node
            
            for edge in node.connections['out']:
                edge_sid = str(id(edge))
                assert edge_sid not in ids_to_edges
                assert edge_sid not in ids_to_nodes
                ids_to_edges[edge_sid] = edge
                
            if sid in n:
                out_nodes[node] = n[sid]
            if sid in e:
                out_edges[node] = e[sid]
    for out_node, dot_edges in out_edges.iteritems():
        edges = {}
        for dot_edge in dot_edges:
            dot_edge['head_node'] = ids_to_nodes[dot_edge['head']]
            # in the "label" we actually save the id of the edge
            # object, see above in generate_dot
            edge_sid = dot_edge['label']
            try:
                edge = ids_to_edges[edge_sid]
            except KeyError:
                # This can happen if we receive a DOT output for a
                # graph that has JUST been modified to NOT include
                # this edge. In that case, ignore the edge.
                continue
            
            assert edge not in edges
            edges[edge] = dot_edge
            
        out_edges[out_node] = edges # replace dot edges with real edges dict
    return g, out_nodes, out_edges
