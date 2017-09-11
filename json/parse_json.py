#!/usr/bin/python
# -*- coding: utf-8 -*-


import json, sys, os
from argparse import Namespace
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

Instance = namedtuple('Pair', ['ref', 'i'])

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

    def run(self):

        '''
            Parse JSON file into a Dictionary
            Use DFS algorithm
        '''
        def path_with_index(s):
            return ("/%s" % s) if type(s) in [str, unicode] else ("[%d]" % s)
        def path_no_index(s):
            return ("/%s" % s) if type(s) in [str, unicode] else ""

        def add_key_value_pair(path, value, i_arr):
            vref = [value]
            ''' Store reference to vaLue in flattened tree'''
            key = "".join(path_with_index(x) for x in path)
            self.flat_tree[key] = vref
            ''' Store reference in typed_values '''
            vtype = "".join(path_no_index(x) for x in path)
            self.data_array[vtype].append(Instance(ref=vref, i=i_arr))

        def parse_tree_to_arrays(obj, obj_path=[], i_arr=[]):
            if type(obj) == list:
                for i, elem in enumerate(obj):
                    parse_tree_to_arrays(elem, obj_path + [i], i_arr + [i])
            elif type(obj) in [OrderedDict]:
                for key, val in obj.items():
                    parse_tree_to_arrays(val, obj_path + [key], i_arr)
            else:
                add_key_value_pair(obj_path, obj, i_arr)

        ''' Parse the JSON tree and generate flat_tree, data_tree '''
        parse_tree_to_arrays(self.input_dict, [self.top_object])


        for k, v in self.flat_tree.items():
            print "%s : %s" % (k, v[0])

        print
        print
        for k, v in self.data_array.items():
            print k
            print v
            print '--'

        #dump_str = json.dumps(self.data_array, indent=2)
        #print dump_str


        '''
        print top_object + "[0].__object_type = " + data_array[0]['__object_type']
        print top_object + "[1].last_name = " + data_array[1]['last_name']
        print top_object + "[1].birth_date.text = " + data_array[1]['birth_date']['text']
        print top_object + "[1].birth_date.structured_date.year = " + str(data_array[1]['birth_date']['structured_date']['year'])
        print top_object + "[2].__object_type = " + data_array[2]['__object_type']
        for i in xrange(len(data_array[2]['children'])):
            print "%s[2].children[%d].child.name = %s" %(top_object, i, data_array[2]['children'][i]['child']['name'])
        '''

#------------
# main
#------------

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        proc = JSON_Processor()
        proc.reset(sys.argv[1])
        proc.run()
    else:
        print 'missing filename. exiting .....'
        print

'''
    WORKING function !!!!

    def recursive_print(obj, obj_path=[]):

        if type(obj) == list:
            for i, elem in enumerate(obj):
                obj_path.append("[%d]" % i)
                recursive_print(elem, obj_path)
                obj_path.pop()
        elif type(obj) in [dict, OrderedDict]:
            for key, val in obj.items():
                obj_path.append("[%s]" % key)
                recursive_print(val, obj_path)
                obj_path.pop()
        else:
            print "%s = %s" % ("".join(obj_path), obj)

'''
'''
    Parse JSON file into a Namespace object

data_obj = json.loads(file_content, object_hook=lambda x: Namespace(**x))
print "Namespace: there are %s JSON objects" % len(data_obj)
print top_object + "[0].__object_type = " + data_obj[0].__object_type
print top_object + "[1].last_name = " + data_obj[1].last_name
print top_object + "[1].birth_date.text = " + data_obj[1].birth_date.text
print top_object + "[1].birth_date.structured_date.year = " + str(data_obj[1].birth_date.structured_date.year)
print top_object + "[2].__object_type = " + data_obj[2].__object_type
for i in xrange(len(data_obj[2].children)):
    print "%s[2].children[%d].child.name = %s" %(top_object, i, data_obj[2].children[i].child.name)
'''
