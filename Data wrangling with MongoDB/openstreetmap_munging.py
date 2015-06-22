# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 17:57:22 2015

@author: juhosalminen1
"""

import re
import xml.etree.cElementTree as ET
from collections import defaultdict
import codecs
import json
from pymongo import MongoClient

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        created = {}
        lon = None
        lat = None
        pos = []
        address = {}
        node_refs = []
        node['type'] = element.tag
        for k in element.keys():
            if k in CREATED:
                created[k] = element.get(k)
            elif k == 'lon':
                lon = float(element.get(k))
            elif k == 'lat':
                lat = float(element.get(k))
            else:
                node[k] = element.get(k)
        if lon != None and lat != None:
            pos = [lat, lon]
        
        for elem in element:
            if elem.tag == 'tag' and not re.search(problemchars, elem.get('k')):
                if re.match('addr:', elem.get('k')):
                    if len(elem.get('k').split(':')) == 2:
                        address[elem.get('k').split(':')[1]] = elem.get('v')
            elif element.tag == 'way' and elem.tag == 'nd':
                node_refs.append(elem.get('ref'))
            else:
                node[elem.get('k')] = elem.get('v')
                
        if len(pos) == 2:
            node['pos'] = pos
        if len(created) > 0:
            node['created'] = created
        if len(address) > 0:
            node['address'] = address
        if len(node_refs) > 0:
            node['node_refs'] = node_refs
        return node
    else:
        return None

def process_map(file_in):
    client = MongoClient("mongodb://localhost:27017")
    db = client.datascience
    for _, element in ET.iterparse(file_in):
        el = shape_element(element)
        if el:
            db.osm.insert(el)
    num_files = db.osm.find().count()
    print('Number of items in db: ' + str(num_files))

'''
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:

                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
'''

process_map('interpreter.osm')
print('hello')