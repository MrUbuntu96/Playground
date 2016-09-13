#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Input:
        Generate communication network for a working group
        N - sze of the group
        Hubs - 10% * N ± 5%
        Max out edges: 30
        Min eges : uniform distribution 0-5

    Output:

'''

import csv, sys, os, re, time, math, random
import numpy as np
from numpy import random as rand


def print_obj(obj):
    attrs = vars(obj)
    print '------'
    print '\n'.join("%s: %s" % item for item in attrs.items())
    print '------'


class Node:
    def __init__(self, id):
        self.id = id
        self.label = str(id)
        self.value = 1
        self.connections = []

    def connect(self, node):
        self.connections.append(node)

    def degree(self):
        return len(self.connections)

    def connected(self, node):
        return node in self.connections


class Edge:
    count = 0
    def __init__(self, _from, _to):
        self._from = _from
        self._to = _to
        self.id = Edge.count
        Edge.count += 1


class Network:
    def __init__(self, size):
        self.node = []
        self.edge = []
        self.size = size

    def add_edge(self, _from, _to):
        self.edge.append(Edge(_from, _to))

    def create_nodes(self):
        for i in xrange(self.size):
            self.node.append(Node(i))

    def create_edge(self, _from, _to):
        from_node = self.node[_from]
        to_node = self.node[_to]
        if _to == _from or from_node.connected(_to):
            # already connected
            return False
        else:
            self.add_edge(_from, _to)
            from_node.connect(_to)
            to_node.connect(_from)
            if from_node.degree() > 9:
                from_node.value = 3
            elif to_node.degree() > 6:
                to_node.value = 2
            #print '%d => %d' % (_from, _to)
            return True

    def generate_random_edges(self):
      for _from in xrange(self.size):
        count = min(rand.random_integers(1, 3) +  (rand.random_integers(1,10) > 8) * 7, self.size-1) - self.node[_from].degree()
        if count > 0:
            connections = 0
            for _to in rand.permutation(self.size):
                if connections < count:
                    if self.create_edge(_from, _to):
                        connections += 1
                else:
                    break

    def dump(self, outf):
        writer = csv.writer(outf)
        writer.writerow( ('node', 'id', 'degree(int)', 'label(string)', 'value(int)') )
        for node in self.node:
            writer.writerow( ('', node.id, len(node.connections), node.label, node.value) )
        writer.writerow( ('' ) )
        writer.writerow( ('edge', 'id', 'from', 'to') )
        for edge in self.edge:
            writer.writerow( ('', edge.id, edge._from, edge._to) )

#        for i in xrange(self.size):
#            outf.write('node %s' % self.node[i].label)
#            outf.write('  => %s\n' % str(self.node[i].connections))


if __name__ == '__main__':
    network = Network(size=16)
    network.create_nodes()
    network.generate_random_edges()
    network.dump(sys.stdout)


'''
    def create_edge(self, _from, _to):
        if _to == _from or _to in self.node[_from].connections:
            # already connected
            return False
        else:
            self.edge.append(Edge(_from, _to))
            self.node[_from].connections.append(_to)
            self.node[_to].connections.append(_from)
            if len(self.node[_from].connections) > 6:
                self.node[_from].value = 2;
            if len(self.node[_to].connections)   > 9:
                self.node[_to].value = 3;
            #print '%d => %d' % (_from, _to)
            return True
'''
