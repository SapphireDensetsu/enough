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

# Parses DOT "plain" output

#   graph scale width height
#   node name x y width height label style shape color fillcolor
#   edge tail head n x1 y1 .. xn yn [label xl yl] style color
#   stop
  
def read_parse(f):
    graph = {}
    nodes = {}
    edges = {} # by heads
    while True:
        line = f.readline()
        words = line.split()
        if words[0] == 'graph':
            graph['scale'], graph['width'], graph['height'] = map(float, words[1:])
            continue

        if words[0] == 'node':
            node = {}
            node['name'] = words[1]
            start = 2
            for i,attr in enumerate(('x', 'y','width', 'height',)):
                node[attr] = float(words[i+start])
            start += 4
            for i,attr in enumerate(('label', 'style',
                                    'shape', 'color',
                                    'fillcolor')):
                node[attr] = (words[i+start])
            
            nodes[node['name']] = node
            continue

        if words[0] == 'edge':
            edge = {}
            edge['tail'] = words[1]
            edge['head'] = words[2]
            n = int(words[3])
            points = []
            i = 4
            while (i - 4) / 2 < n:
                points.append((float(words[i]), float(words[i+1])))
                i += 2
            edge['points'] = points
            edge['style'] = words[-2]
            edge['color'] = words[-1]
            edges.setdefault(edge['tail'], []).append(edge)
            continue

        if words[0] == 'stop':
            break

        raise ValueError("Unexpected statement", line)
    return graph, nodes, edges
            

class Dot(object):
    def __init__(self, command_line='dot'):
        import subprocess
        self.popen = subprocess.Popen((command_line, '-Tplain', '-y'),
                                      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get_graph_data(self, dot_graph_text):
        self.popen.stdin.write(dot_graph_text + '\n')
        return read_parse(self.popen.stdout)
        
