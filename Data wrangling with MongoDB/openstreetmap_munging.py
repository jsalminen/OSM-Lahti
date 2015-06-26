# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 17:57:22 2015

@author: juhosalminen1
"""

import re
import xml.etree.cElementTree as ET
import codecs
import json
from pymongo import MongoClient

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

CITIES = {'LAHTIS': 'Lahti',
          'HOLLOLA': 'Hollola'}

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # Lists and dictionaries to store data        
        created = {}
        lon = None
        lat = None
        pos = []
        address = {}
        node_refs = []
        
        # Get node type
        node['type'] = element.tag 
        
        # Collect data related to document creation and put in dictionary
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
        
        # Iterate over the sub-elements named 'tag', ignore  elements with 
        # problematic characters
        for elem in element:
            if elem.tag == 'tag' and not re.search(problemchars, elem.get('k')):
                # Fix post codes
                if re.match('addr:postcode', elem.get('k')):
                    try:
                        postcode = re.search(r'[0-9]{5}', elem.get('v')).group(0)
                        address['postcode'] = postcode
                    except:
                        address['postcode'] = elem.get('v')
                # Fix cities
                elif re.match('addr:city', elem.get('k')):
                    city = elem.get('v')
                    if city in CITIES:
                        city = CITIES[city]
                    address['city'] = city
                # Change streetnumbers to housenumbers
                elif re.match('addr:streetnumber', elem.get('k')):
                    address['housenumber'] = elem.get('v')
                # Collect the other address elements (only one ':')                
                elif re.match('addr:', elem.get('k')):
                    if len(elem.get('k').split(':')) == 2:
                        address[elem.get('k').split(':')[1]] = elem.get('v')
                # Rest of the elemens are just added to node
                else:
                    node[elem.get('k')] = elem.get('v')
            # Collect node references of ways
            elif element.tag == 'way' and elem.tag == 'nd':
                node_refs.append(elem.get('ref'))
            
        
        # Add position list to node        
        if len(pos) == 2:
            node['pos'] = pos
        # Add created dictionary to node
        if len(created) > 0:
            node['created'] = created
        # Add address dictionary to node
        if len(address) > 0:
            node['address'] = address
        # Add node references to node
        if len(node_refs) > 0:
            node['node_refs'] = node_refs
        return node
    else:
        return None

def process_map_mongo(file_in, host = "mongodb://localhost:27017"):
    # Connect to MongoDB    
    client = MongoClient(host)
    db = client.datascience
    # Parse elements in file, reshape, and insert to MongoDB
    for _, element in ET.iterparse(file_in):
        el = shape_element(element)
        if el:
            db.osm.insert(el)
    num_files = db.osm.find().count()
    print('Number of items in db: ' + str(num_files))


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:

                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")


process_map('lahti_finland.osm')
print('done')