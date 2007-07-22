# Parses DOT "plain" output

#   graph scale width height
#   node name x y width height label style shape color fillcolor
#   edge tail head n x1 y1 .. xn yn [label xl yl] style color
#   stop
  
def read_parse(f):
    graph = {}
    nodes = []
    edges = []
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
            
            nodes.append(node)
            continue

        if words[0] == 'edge':
            edge = {}
            edge['tail'] = words[1]
            edge['head'] = words[2]
            n = words[3]
            points = []
            for i in xrange(int(n)):
                points.append((float(words[i+4]), float(words[i+5])))
            edge['points'] = points
            edge['style'] = words[-2]
            edge['color'] = words[-1]
            edges.append(edge)
            continue

        if words[0] == 'stop':
            break

        raise ValueError("Unexpected statement", line)
    return graph, nodes, edges
            

class DOT(object):
    def __init__(self, command_line='dot'):
        import subprocess
        self.popen = subprocess.Popen((command_line, '-Tplain'),
                                      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get_graph_data(self, dot_graph_text):
        self.popen.stdin.write(dot_graph_text + '\n')
        return read_parse(self.popen.stdout)
        
