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

class GraphGeneratorParams:
    def __init__(self,
                 size=100,
                 samples=100000,
                 sigma=0.1,
                 max_edges=30,
                 hub_percent=0.15,
                 hub_percent_variation=0.05,
                 default_edges=3):
        self.size = size
        self.samples = samples
        self.sigma = sigma
        self.max_edges = max_edges
        self.hub_percent = hub_percent
        self.hub_percent_variation = hub_percent_variation
        self.default_edges = default_edges

debug = True

def print_obj(obj):
    attrs = vars(obj)
    print '------'
    print '\n'.join("%s: %s" % item for item in attrs.items())
    print '------'

def generate_network(prm):

    def histogram_standard_normal(mu, sigma, mn, mx, size):
        return np.histogram(mu + sigma * np.random.standard_normal(prm.samples),
                            bins=size, range=(mn, mx))[0]

    def normalize_histogram_func(elem, max_val):
        ''' this function is used elementwise as input to np.vectorize '''
        return int(round(float(elem) * prm.max_edges / max_val))

    normalize_histogram = np.vectorize(normalize_histogram_func)

    # define range of population (standard distribution)
    mn, mx = -prm.size/2, prm.size/2
    # Create a base histogram with large variance
    base_hist = histogram_standard_normal(0, prm.sigma * 10, mn, mx, prm.size)

    hist = base_hist
    # Get a number of hubs = nodes with high connectivity.
    hub_pos = np.empty(int(np.round(prm.size * (prm.hub_percent + prm.hub_percent_variation * (2 * np.random.rand() - 1.0) ))), dtype=int)
    #if debug: print 'n_hubs=%d' % n_hubs
    # For each hub create a spike (very narrow standard distribution)
    for i in xrange(len(hub_pos)):
        # 3 sigma from the
        hub_spike = histogram_standard_normal(0, prm.sigma, mn, mx, prm.size)
        hub_pos[i] = random.randint(mn, mx)

        # cycle the spike to a random position
        hist = hist + np.roll(hub_spike, hub_pos[i])
        #if debug: print temp

    f_elem = np.vectorize(normalize_histogram_func)
    arr = f_elem(hist, max(hist))
    if sum(arr) % 2 == 1:
        arr[0] = arr[0] + 1
    if debug: print_obj(prm)
    if debug: print 'hubs:', hub_pos
    print arr
    #print np.sort(arr)[::-1] # [::-1] = reverse the array for descending sort
    if debug: pass
    print 'sum=%d, mean=%.2f, median=%.2f, std=%.2f' % (sum(arr), np.mean(arr), np.median(arr), np.std(arr))
    print
    #hh = histogram_standard_normal(0, prm.sigma * 10, -arr[0], arr[0], )

    # randomize the degree of zero nodes
    #if n <= prm.max_edges - prm.default_edges:
    #    n = min(prm.max_edges, n + random.randint(1, prm.default_edges))


#------------
# main
#------------
if __name__ == '__main__':
    p = GraphGeneratorParams()
    generate_network(p)
    p = GraphGeneratorParams(samples=100)
    generate_network(p)
    p = GraphGeneratorParams(size=30, max_edges=20)
    generate_network(p)
    p = GraphGeneratorParams(size=30, max_edges=20, samples=100)
    generate_network(p)
