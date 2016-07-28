# -*- coding: utf-8 -*-
import csv, sys, os, re
from lxml import etree

master_key_dict = {'node': {}, 'edge':{} }

g_id = 0;
def get_id():
    global g_id
    g_id += 1
    return str(g_id)

def start_attrib_index(mode):
    return 2 if mode == 'node' else 4

def add_keys(mode, header, parent):
    '''
        <key id="name" for="node" attr.name="name" attr.type="string"/>
    '''
    for i in range(start_attrib_index(mode), len(header)):
        if len(header[i]) == 0: continue
        attrs = re.split('\(|\)', header[i])
        key = etree.SubElement(parent, 'key')
        key.attrib['id'] = attrs[0]
        key.attrib['for'] = mode
        key.attrib['attr.name'] = attrs[0]
        key.attrib['attr.type'] = attrs[1]
        #print etree.tostring(key, pretty_print=True)
        #print i
        parent.append(key)
        master_key_dict[mode][i] = attrs[0]

def add_element(mode, row, parent):
    '''
        <node id="6">
          <data key="labelV">person</data>
          <data key="name">peter</data>
          <data key="age">35</data>
        </node>
        <edge id="7" source="1" target="2">
          <data key="labelE">knows</data>
          <data key="weight">0.5</data>
        </edge>
    '''
    graph_element = etree.SubElement(parent, mode)
    graph_element.attrib['id'] = get_id() #row[1]
    if mode == 'edge':
        graph_element.attrib['source'] = row[2]
        graph_element.attrib['target'] = row[3]
    # Parse attributes
    for i in range(start_attrib_index(mode), len(row)):
        if len(row[i]) == 0: continue # sometimes there's an empty element at the end
        data = etree.SubElement(graph_element, 'data')
        #print '==> mode=%s, i=%d, val=%s' % (mode, i, row[i])
        data.attrib['key'] = master_key_dict[mode][i]
        data.text = row[i].decode('utf-8')
        graph_element.append(data)

    parent.append(graph_element)


def csv_2_graphml(input_file):

    csv_file = open(input_file)
    csv_reader = csv.reader(csv_file)

    # Create graph element
    graphml_root = etree.Element('graphml')
    graph = etree.Element('graph')
    graph.attrib['id'] = 'G'
    graph.attrib['edgedefault'] = 'directed'
    mode = ''

    # Parse rows
    for row in csv_reader:
        # Skip blank rows
        if len(row) > 0:
            if row[0] == 'node' or row[0] == 'edge':
                # Start edge or node section
                mode = row[0]
                add_keys(mode, row, graphml_root)
            elif row[0] == '' and mode != '':
                # Add Element (node or edge)
                add_element(mode, row, graph)

    graphml_root.append(graph)
    return etree.tostring(graphml_root, pretty_print=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'missing filename. exiting .....'
        print
    else:
        input_file = os.path.basename(sys.argv[1])
        base_filename = os.path.splitext(input_file)[0]
        xml_str = csv_2_graphml(base_filename + '.csv')
        xml_output_file = open(base_filename + '.xml', 'w')
        xml_output_file.write(xml_str)
        xml_output_file.close()
