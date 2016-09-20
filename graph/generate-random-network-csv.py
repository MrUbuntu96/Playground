#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Input:
        Generate communication network for a working group
        N - size of the group
        Hubs - 10% * N ± 5%
        Max out edges: 30
        Min eges : uniform distribution 0-5

    Output:

'''

import csv, sys, os, re, time, math, random, argparse
import numpy as np
from numpy import random as rand


def print_obj(obj):
    attrs = vars(obj)
    print '------'
    print '\n'.join("%s: %s" % item for item in attrs.items())
    print '------'

def condition(n, p):
    return n if rand.random() > p else 0

class Node:
    def __init__(self, id):
        self.id = id
        self.label = str(id)
        self.value = 1
        self.connections = []

    def degree(self):
        return len(self.connections)

    def connect(self, node):
        self.connections.append(node)
        self.value = 1 + self.degree() / 3
        self.label = '%d(%d)' %(self.id, self.degree())

    def is_connected(self, node):
        return node in self.connections


class Edge:
    count = 1
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node
        self.id = Edge.count
        Edge.count += 1


class Network:
    def __init__(self, size, low, high, spike, prob):
        self.node = []
        self.edge = []
        self.size = size
        self.edges_low  = low
        self.edges_high = high
        self.edges_spike = spike
        self.spike_prob = prob

    def generate(self):

        def create_nodes():
            for i in xrange(self.size):
                self.node.append(Node(i))

        def get_edge_count(node):
            base = rand.random_integers(self.edges_low, self.edges_high)
            return min(base +  condition(self.edges_spike, self.spike_prob), self.size-1) - node.degree()

        def create_edge(from_node, to_node):
            self.edge.append(Edge(from_node, to_node))
            from_node.connect(to_node)
            to_node.connect(from_node)
            #print '%d => %d' % (_from, _to)

        # start here
        create_nodes()

        for _from in xrange(self.size):
        #    print 'from=%d' % _from
            from_node = self.node[_from]
            n = get_edge_count(from_node)
            if n > 0:
                connections = 0
                for _to in rand.permutation(self.size):
                #    print 'to=%d' % _to
                    to_node = self.node[_to]
                    if _to != _from and not from_node.is_connected(to_node):
                        create_edge(from_node, to_node)
                        connections += 1
                        if connections == n:
                            break

    def dump(self, outf):
        writer = csv.writer(outf)
        writer.writerow( ('NODE', 'id(int)', 'degree(int)', 'label(string)', 'value(int)') )
        for node in self.node:
            writer.writerow( ('', node.id, len(node.connections), node.label, node.value) )
        writer.writerow( ('' ) )
        writer.writerow( ('EDGE', 'id(int)', 'from(int)', 'to(int)') )
        for edge in self.edge:
            writer.writerow( ('', edge.id, edge.from_node.id, edge.to_node.id) )

#        for i in xrange(self.size):
#            outf.write('node %s' % self.node[i].label)
#            outf.write('  => %s\n' % str(self.node[i].connections))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example with non-optional arguments')
    parser.add_argument('--size',   type=int, dest='size', default=20)
    parser.add_argument('--low',    type=int, dest='low', default=1)
    parser.add_argument('--high',   type=int, dest='high', default=3)
    parser.add_argument('--spike',  type=int, dest='spike', default=7)
    parser.add_argument('--prob',   type=float, dest='prob', default=0.8)
    args = parser.parse_args()

    sys.stderr.write(str(args) + '\n\n')

    network = Network(  size = args.size,
                        low = args.low,
                        high = args.high,
                        spike = args.spike,
                        prob = args.prob )
    network.generate()
    network.dump(sys.stdout)
