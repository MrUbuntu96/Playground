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

INDEX = '_i_'

Instance = namedtuple('Pair', ['ref', 'ilist'])

class JSON_Processor:
    '''
        file ==> input_dict (Ordered)
        input_dict ==> flattened_tree (Ordered)
        input_dict ==> typed_values

    '''
    def __init__(self):
        self.top_object = ''
        self.file_content = ''
        self.input_dict = OrderedDict
        self.flat_tree  = OrderedDict()
        self.data_array = defaultdict(list)
        self.dfs_level = 0


    def reset(self, filename):
        self.__init__()
        self.top_object = os.path.basename(filename).split('.')[0] # filename w/o extension
        self.file_content = open(filename).read()
        self.input_dict = json.loads(self.file_content, object_pairs_hook = OrderedDict)

    def run(self):

        '''
            Parse JSON file into a Dictionary
            Use DFS algorithm
        '''
        def is_str(s):
            return True if type(s) in [str, unicode] else False

        def add_key_value_pair(path, value, ilist):
            vref = [value]
            ''' Store reference to vaLue in flattened tree'''
            key = "".join(("/%s" % x) if is_str(x) else ("[%d]" % x) for x in path)
            self.flat_tree[key] = vref
            ''' Store reference in typed_values '''
            vtype = "".join(("/%s" % x) if is_str(x) else "" for x in path)
            self.data_array[vtype].append(Instance(ref=vref, ilist=ilist))

        def parse_tree_to_arrays(obj, obj_path=[], ilist=[]):

            self.dfs_level += 1
            if type(obj) == list:
                for i, elem in enumerate(obj):
                    parse_tree_to_arrays(elem, obj_path + [i], ilist + [i])
            elif type(obj) in [OrderedDict]:
                for key, val in obj.items():
                    parse_tree_to_arrays(val, obj_path + [key], ilist)
            else:
                add_key_value_pair(obj_path, obj, ilist)

            #self.dfs_level -=1
            #if self.dfs_level == 0:
            #    print 'DONE'
            #    return parse_tree

            #for i, elem in enumerate(data_array):
            #recursive_print(elem, obj_path + ["[%d]" % i])

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
