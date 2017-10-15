#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, sys, os, traceback
from collections import OrderedDict, defaultdict

'''
What this script does?
    1) load a JSON file
    2) output an equivalent flat tree structure of the file

Sample run: ./parse_json.py genealogy.json
'''

class JSON_Processor:
    '''
        1) Load JSON file into a dict
            >>> file ==> input_dict (Ordered)
        2) Store JSON file as a flat tree, used to reconstruct the original file after manipulation
            >>> input_dict ==> flat_tree (Ordered)
        3) Store all data as a dict of key/[list of values]
            Key include the path from root
            All values for the same keys are stored in a list
            >>> input_dict ==> data_map
        4) JSON unmarshalling rules
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
    def __init__(self):
        self.top_object = ''
        self.input_dict = OrderedDict
        self.flat_tree  = OrderedDict()
        self.data_map = defaultdict(list)

    def reset(self, filename):
        self.__init__()
        self.top_object_name = os.path.basename(filename).split('.')[0] # filename w/o extension
        self.input_dict = json.loads(open(filename).read(), object_pairs_hook = OrderedDict)

    class Data_Instance:
        '''
            This class contains a value and a list of indices
        '''
        def __init__(self, ref, i_arr):
            ''' A reference to the data value '''
            self.ref_to_val = ref
            ''' An array of indices that point to the data value '''
            self.i_arr = i_arr

    def parse_tree_to_arrays(self, obj, obj_path=[], i_arr=[]):
        def add_key_value_pair(path, value, i_arr):
            def data_path(s):
                ''' Specific for each key/value pair, contains indices of instance within list '''
                return "".join((("/%s" % s) if type(s) in [str, unicode] else ("[%d]" % s)) for s in path)
            def property_path(s):
                ''' Property path starting from root, can point to multiple values with the same key '''
                return "".join((("/%s" % s) if type(s) in [str, unicode] else "") for s in path)

            ''' User reference to value (instead of value itself) '''
            ref_to_val = [value]
            data_instance = JSON_Processor.Data_Instance(ref_to_val, i_arr)
            self.flat_tree[data_path(path)] = ref_to_val
            self.data_map[property_path(path)].append(data_instance)
        # --
        if type(obj) == list:
            for i, elem in enumerate(obj):
                self.parse_tree_to_arrays(elem, obj_path + [i], i_arr + [i])
        elif type(obj) == OrderedDict:
            for key, val in obj.items():
                self.parse_tree_to_arrays(val, obj_path + [key], i_arr)
        else:
            ''' A key-value pair '''
            add_key_value_pair(obj_path, obj, i_arr)

    def run(self):
        '''
            Parse JSON file into a Dictionary
            Use DFS algorithm
            Create flat_tree for JSON reconstruction
            Create data_map for data manipulation: statistical analysis, security check
        '''
        self.parse_tree_to_arrays(self.input_dict, []) #[self.top_object_name])

    def print_output(self):
        def print_title(s):
            print s
            print '=' * len(s)

        print_title('JSON file as a flattened tree')
        for k, v in self.flat_tree.items():
            print "%s : %s" % (k, v[0])
        print '--\n' * 4
        #
        print_title('Map of all properties in JSON file')
        for k, v in self.data_map.items():
            print "%s: %d items" % (k, len(v))
        print '--\n' * 4
        #
        print_title('Map of all values in JSON file')
        for k, v in self.data_map.items():
            print '%s (%d items): ' % (str(k), len(v)),
            for i in xrange(min(3, len(v))):
                print '%s: %s,' % (str(v[i].ref_to_val[0]), str(v[i].i_arr)),
            print '....' if len(v)>3 else ''

#------------
# main
#------------

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    processor = JSON_Processor()
    processor.reset(sys.argv[1])
    processor.run()
    processor.print_output()


if __name__ == '__main__':
    try:
        main()
    except (ValueError, Exception) as e:
        #print e
        print
        print traceback.format_exc()
        print 'Duh!!! Program exited'
        print
