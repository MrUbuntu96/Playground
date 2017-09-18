#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, sys, os
from collections import OrderedDict, defaultdict, namedtuple

'''
JSON decoding

    JSON	    Python
    -------------------
    object	=>  dict
    array	=>  list
    string	=>  str
    int     =>  int
    real	=>  float
    true	=>  True
    false	=>  False
    null	=>  None
'''

Key_Value_Pair = namedtuple('Pair', ['ref', 'i'])

class JSON_Processor:
    '''
        file ==> input_dict (Ordered)
        input_dict ==> flat_tree (Ordered)
        input_dict ==> data_array
    '''
    def __init__(self):
        self.top_object = ''
        self.input_dict = OrderedDict
        self.flat_tree  = OrderedDict()
        self.data_array = defaultdict(list)

    def reset(self, filename):
        self.__init__()
        self.top_object = os.path.basename(filename).split('.')[0] # filename w/o extension
        self.input_dict = json.loads(open(filename).read(), object_pairs_hook = OrderedDict)


    def parse_tree_to_arrays(self, obj, obj_path=[], i_arr=[]):

        def add_key_value_pair(path, value, i_arr):

            def path_with_index(s):
                return ("/%s" % s) if type(s) in [str, unicode] else ("[%d]" % s)
            def path_no_index(s):
                return ("/%s" % s) if type(s) in [str, unicode] else ""

            ''' User reference to value (instead of value itself) '''
            vref = [value]
            key = "".join(path_with_index(x) for x in path)
            self.flat_tree[key] = vref
            vtype = "".join(path_no_index(x) for x in path)
            self.data_array[vtype].append(Key_Value_Pair(ref=vref, i=i_arr))

        if type(obj) == list:
            for i, elem in enumerate(obj):
                self.parse_tree_to_arrays(elem, obj_path + [i], i_arr + [i])
        elif type(obj) in [OrderedDict]:
            for key, val in obj.items():
                self.parse_tree_to_arrays(val, obj_path + [key], i_arr)
        else:
            add_key_value_pair(obj_path, obj, i_arr)

    def run(self):
        '''
            Parse JSON file into a Dictionary
            Use DFS algorithm
            Create flat_tree for JSON reconstruction
            Create data_array for statistical data manipulation
        '''

        ''' START HERE '''
        ''' Parse the JSON tree and generate flat_tree, data_tree '''
        self.parse_tree_to_arrays(self.input_dict, []) #[self.top_object])

        for k, v in self.data_array.items():
            print "%s: %d items" % (k, len(v))
        print '--\n' * 4
        for k, v in self.flat_tree.items():
            print "%s : %s" % (k, v[0])
        print '--\n' * 4
        for k, v in self.data_array.items():
            print '%s (%d items): ' % (str(k), len(v)),
            for i in xrange(min(10, len(v))):
                print '%s: %s,' % (str(v[i].ref[0]), str(v[i].i)),
#                print str(v[i]) + ',',
            print '....\n' if len(v)>10 else '' + '\n--'

#------------
# main
#------------

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')

    if len(sys.argv) >= 2:
        try:
            proc = JSON_Processor()
            proc.reset(sys.argv[1])
            proc.run()
        except ValueError as e:
            print e
            print 'Program exited'
    else:
        print 'missing filename. exiting .....'
        print
