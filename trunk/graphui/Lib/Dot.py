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

from twisted.internet import protocol, defer
from twisted.protocols.basic import LineReceiver

class OutOfDate(Exception): pass

class _ProtocolWrapper(protocol.ProcessProtocol):
    """
    This class wraps a L{Protocol} instance in a L{ProcessProtocol} instance.
    """
    def __init__(self, proto):
        self.proto = proto

    def connectionMade(self):
        self.proto.connectionMade()

    def outReceived(self, data):
        self.proto.dataReceived(data)

    def errReceived(self, data):
        import sys
        sys.stderr.write(data)

    def processEnded(self, reason):
        self.proto.connectionLost(reason)


class _DotProtocol(LineReceiver):
    delimiter = '\n'
    def __init__(self):
        self.waiting = None
        self._current_graph_parser = None
        self._process = None

    def set_process(self, process):
        self._process = process

    def lineReceived(self, line):
        if self._current_graph_parser is None:
            raise Error("Dot outputs stuff, we're not expecting it", line)
        self._current_graph_parser.lineReceived(line)

    def _completed_current(self, result):
        self._current_graph_parser = None
        if self.waiting:
            dot_graph_text, d = self.waiting
            self.waiting = None
            self._start(dot_graph_text, d)
        return result

    def get_graph_data(self, dot_graph_text):
        d = defer.Deferred()
        d.addBoth(self._completed_current)
        if self._current_graph_parser:
            # Let the current result finish computing, "queue" this
            # one.
            if self.waiting:
                self.waiting[1].errback(OutOfDate())
            self.waiting = dot_graph_text, d
        else:
            self._start(dot_graph_text, d)
        return d

    def _start(self, dot_graph_text, d):
        self._process.write(dot_graph_text + '\n')
        self._current_graph_parser = _GraphParser(d)

class _GraphParser(object):
    def __init__(self, dresult):
        self.dresult = dresult
        self.graph = {}
        self.nodes = {}
        self.edges = {} # by heads

    def lineReceived(self, line):
        graph, nodes, edges = self.graph, self.nodes, self.edges
        words = line.split()
        if words[0] == 'graph':
            graph['scale'], graph['width'], graph['height'] = map(float, words[1:])
            return

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
            return

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
            if len(words) == 6+n*2:
                edge['label'] = edge['lx'] = edge['ly'] = None
            elif len(words) == 9+n*2:
                edge['label'] = edge[-5]
                edge['lx'], edge['ly'] = edge[-4], edge[-3]
            else:
                assert False, "Cannot understand %r" % (line,)
            edge['style'] = words[-2]
            edge['color'] = words[-1]
            edges.setdefault(edge['tail'], []).append(edge)
            return

        if words[0] == 'stop':
            self.dresult.callback((graph, nodes, edges))
            return

        self.dresult.errback(ValueError("Unexpected statement", line))
            

class Dot(object):
    def __init__(self, command_line='dot'):
        from twisted.internet import reactor
        self.protocol = _DotProtocol()
        self.process = reactor.spawnProcess(_ProtocolWrapper(self.protocol),
                                            command_line, [command_line, '-Tplain', '-y'])
        self.protocol.set_process(self.process)

    def get_graph_data(self, dot_graph_text):
        return self.protocol.get_graph_data(dot_graph_text)
