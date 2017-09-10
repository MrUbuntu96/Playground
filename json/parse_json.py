#!/usr/bin/python
# -*- coding: utf-8 -*-


import json, sys, os
from argparse import Namespace
from collections import OrderedDict, defaultdict

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



def process_json(filename):

    '''
        Parse JSON file into a Dictionary
    '''
    parsed_json = OrderedDict()
    types_dict  = defaultdict()

    # Custom exception
    class JSONProcessingException(Exception):
        def __str__(self):
            return repr(" >>> JSON error: expecting a list of objects at top level.")

    def append_key_value_pair(key, value):
        if key not in types_dict: types_dict[key] = []
        types_dict[key].append(value)

    def recursive_print(obj, obj_path=[]):
        if type(obj) == list:
            for i, elem in enumerate(obj):
                recursive_print(elem, obj_path + ["[%d]" % i])
        elif type(obj) in [dict, OrderedDict]:
            for key, val in obj.items():
                recursive_print(val, obj_path + ["[%s]" % key])
        else:
            path = "".join(obj_path)
            parsed_json[path] = obj
            append_key_value_pair(path, obj)

    top_object = os.path.basename(filename).split('.')[0] # filename w/o extension
    data_array = json.loads(open(filename).read(), object_pairs_hook = OrderedDict)

    if type(data_array) != list:
        raise JSONProcessingException()

    #for i, elem in enumerate(data_array):
    #    recursive_print(elem, obj_path + ["[%d]" % i])

    recursive_print(data_array, [top_object])
    dump_str = json.dumps(parsed_json, indent=2)
    print dump_str
    dump_str = json.dumps(types_dict, indent=2)
    print dump_str

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
        filename = sys.argv[1]
        process_json(filename)
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
