# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:14:01 2015

@author: juhosalminen1
"""

import re
import xml.etree.cElementTree as ET

timestamp_re = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}[A-Z][0-9]{2}:[0-9]{2}:[0-9]{2}Z')

def audit(filename):
    uids = set()
    missing_uids = 0
    wrong_ids = 0
    wrong_timestamps = 0
    wrong_coords = 0
    wrong_ways = 0
    tags = set()
    street_abreviations = set()
    
    for _, element in ET.iterparse(filename):
        if element.tag in ['node', 'way', 'relation']:
             # Count unique users and check for missing uids
            if element.get('uid'):
                uids.add(element.get('uid'))
            else: 
                missing_uids += 1
        
            # Check ids exist and are integers
            try:
                int(element.get('id'))
            except:
                wrong_ids += 1
            
            # Check timestamp is in correct format
            if not re.match(timestamp_re, element.get('timestamp')):
                wrong_timestamps += 1
            
            # Count and list unique tag names
            for elem in element:
                if elem.tag == 'tag':
                    tags.add(elem.get('k'))

            # Check for abbreviations in street names            
            for elem in element:
                if elem.tag == 'tag' and re.match('addr:', elem.get('k')):
                    if re.search('\.', elem.get('v')):
                        street_abreviations.add(elem.get('v'))
            
        # Check latitude and longitude are floats
        if element.tag == 'node':
            try: 
                float(element.get('lat'))
                float(element.get('lon'))
            except:
                wrong_coords += 1
        
        # Check ways have more than 1 node reference
        if element.tag == 'way':
            nd_count = 0
            for elem in element:
                if elem.tag == 'nd':
                    nd_count += 1
            if nd_count < 2:
                wrong_ways += 1
                    
            
    print('number of unique uids: ' + str(len(uids)))
    print('missing uids: ' + str(missing_uids))
    print('wrong ids: ' + str(wrong_ids))
    print('wrong timestamps: ' + str(wrong_timestamps))
    print('wrong longitude or latitude: ' + str(wrong_coords))
    print('ways with less than 2 node references: ' + str(wrong_ways))
    print('number of street abbreviations: ' + str(len(street_abreviations)))
    print(street_abreviations)
    print('number of unique tag names: ' + str(len(tags)))
    print(tags)


audit('helsinki_finland.osm')


















