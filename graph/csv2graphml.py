#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Input:
        Graph in CSV format

    Output:
        Graph in graphml format

        <graphml>
            <key id="type" for="node" attr.name="type" attr.type="string"/>
            ...
            <key id="relation" for="edge" attr.name="relation" attr.type="string"/>
            ...
            <graph id="G" edgedefault="directed">
                <node id="6">
                    <data key="labelV">person</data>
                    <data key="name">peter</data>
                    <data key="age">35</data>
                </node>
                <edge id="7" source="1" target="2">
                    <data key="labelE">knows</data>
                    <data key="weight">0.5</data>
                </edge>
                ...
            </graph>
        </graphml>
'''

import csv, sys, os, re
from lxml import etree

KEYS_DICT = {'node': {}, 'edge':{} }
NODE_START_COL = 2
EDGE_START_COL = 4
EDGE_ID_COL    = 1
SOURCE_NODE_COL = 2
TARGET_NODE_COL = 3

def csv_2_graphml(input_file):

    #
    #----beginning-of-inner-functions-----
    #
    def start_column(element_type):
        '''
            return the column index where key/value pairs start in the CSV table
        '''
        return NODE_START_COL if element_type == 'node' else EDGE_START_COL

    def add_keys(header, element_type, parent):
        '''
            csv:
                node,type(string),name(string),
            graphML:
                <key id="type" for="node" attr.name="type" attr.type="string"/>
                <key id="name" for="node" attr.name="name" attr.type="string"/>
        '''
        for i in range(start_column(element_type), len(header)):
            if len(header[i]) == 0: continue
            (attr_name, attr_type, foo) = re.split('\(|\)', header[i]) # name(string)
            key = etree.SubElement(parent, 'key')
            key.attrib['id'] = attr_name
            key.attrib['for'] = element_type
            key.attrib['attr.name'] = attr_name
            key.attrib['attr.type'] = attr_type
            KEYS_DICT[element_type][i] = attr_name
            parent.append(key)

    def add_element(row, element_type, parent):
        '''
            <node id="6">
                <data key="labelV">person</data>
                <data key="name">peter</data>
            </node>

            OR

            <edge id="7" source="1" target="2">
                <data key="labelE">knows</data>
                <data key="weight">0.5</data>
            </edge>
        '''

        graph_element = etree.SubElement(parent, element_type)
        graph_element.attrib['id'] = row[EDGE_ID_COL]
        if element_type == 'edge':
            # First two column keys in csv are source and target
            graph_element.attrib['source'] = row[SOURCE_NODE_COL]
            graph_element.attrib['target'] = row[TARGET_NODE_COL]
        # Parse attributes
        for i in range(start_column(element_type), len(row)):
            if len(row[i]) == 0: continue # sometimes there's an empty element at the end
            data = etree.SubElement(graph_element, 'data')
            data.attrib['key'] = KEYS_DICT[element_type][i]
            data.text = row[i].decode('utf-8')
            graph_element.append(data)
        #
        parent.append(graph_element)
    #
    #----end-of-inner-functions-----
    #

    #
    #----function-csv_2_graphml-starts-here-----
    #
    csv_file = open(input_file)
    csv_reader = csv.reader(csv_file)

    # Create graph element
    graphml_root = etree.Element('graphml')
    graph_root = etree.Element('graph')
    graph_root.attrib['id'] = 'G'
    graph_root.attrib['edgedefault'] = 'directed'
    element_type = ''

    # Parse rows
    for row in csv_reader:
        # Skip blank rows
        if len(row) > 0:
            if row[0] == 'node' or row[0] == 'edge':
                # Start edge or node section
                element_type = row[0]
                add_keys(row, element_type, graphml_root)
            elif row[0] == '' and element_type != '':
                # Add Element (node or edge)
                add_element(row, element_type, graph_root)

    graphml_root.append(graph_root)
    return etree.tostring(graphml_root, pretty_print=True)
    #
    #----end-of-csv_2_graphml-----
    #


#------------
# main
#------------
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        input_file = os.path.basename(sys.argv[1])
        base_filename = os.path.splitext(input_file)[0]
        print '\nConverting movies.csv ==> movies.xml (graphML) .....',
        xml_str = csv_2_graphml(base_filename + '.csv')
        xml_output_file = open(base_filename + '.xml', 'w')
        xml_output_file.write(xml_str)
        xml_output_file.close()
        print 'done\n'
    else:
        print 'missing filename. exiting .....'
        print
