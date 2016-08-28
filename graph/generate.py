#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Input:
        Generate communication network for a working group
        N - sze of the group
        Hubs - 10% * N ± 5%
        Max out edges: 30
        Min eges : unfirm distribution 0-5

    Output:

'''

import csv, sys, os, re, time, math
import numpy as np


GROUP_SIZE = [100]
HUB_SIGMA = 1.0 # narrow
NUM_SAMPLES = 100000



def generate_network():

    def histo_normal_dist(mu, sigma, mn, mx, size):
        return np.histogram(mu + sigma * np.random.standard_normal(NUM_SAMPLES),
                            bins=size, range=(mn, mx))[0]

    for group_size in GROUP_SIZE:
        mn, mx = -group_size/2, group_size/2
        #hist = [0] * group_size
        hist = histo_normal_dist(0, HUB_SIGMA * 8, mn, mx, group_size)
        i = 0
        n_hubs = int(group_size * (0.1 + 0.01 * np.random.randint(-3, 4)))
        print 'n_hubs=%d' % n_hubs
        for h in xrange(n_hubs):
            hub_pos = np.random.randint(group_size - 6*HUB_SIGMA) + 3*HUB_SIGMA
            print 'hub_pos[%d]=%d' % (i, hub_pos)
            hist = hist + histo_normal_dist(hub_pos, HUB_SIGMA, mn, mx, group_size)
            print hist
            i += 1
            print
        print '--------------------'
        hist = hist * 30.0 / max(hist)
        print hist

#------------
# main
#------------
if __name__ == '__main__':
    generate_network()
