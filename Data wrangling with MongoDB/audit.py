# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:14:01 2015

@author: Juho Salminen
"""

import re
import xml.etree.cElementTree as ET

# Regurlar expression to match correct timestamp format
timestamp_re = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}[A-Z][0-9]{2}:[0-9]{2}:[0-9]{2}Z')

# Regular expression to match expected street names
street_re = re.compile(r'.*tie|.*katu|.*kuja|.*aukio|.*polku|.*väylä|.*raitti|.*rinne|.*mutka|.*piha|.*tori|.*kulma|.*kaari')

def audit(filename):
    # Variables to store audit results
    uids = set()
    missing_uids = 0        
    wrong_ids = 0
    wrong_timestamps = 0
    wrong_coords = 0
    wrong_ways = 0
    tags = set()
    street_abreviations = set()
    wrong_postcodes = []
    cities = set()
    weird_numbers = []
    weird_streets = []
    
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
                if elem.tag == 'tag' and re.match('addr:street', elem.get('k')):
                    if re.search('\.', elem.get('v')):
                        street_abreviations.add(elem.get('v'))
            
            # Check for unexpected street names           
            for elem in element:
                if elem.tag == 'tag' and re.match('addr:street', elem.get('k')):
                    if not re.search(street_re, elem.get('v')):
                        weird_streets.append(elem.get('v'))
            
            # Check postal codes
            for elem in element: 
                if elem.tag == 'tag' and re.match('addr:postcode', elem.get('k')):
                    if not re.match(r'(00|01)[0-9]{3}\Z', elem.get('v')):
                        wrong_postcodes.append(elem.get('v'))
            
            # Check city
            for elem in element: 
                if elem.tag == 'tag' and re.match('addr:city', elem.get('k')):
                    cities.add(elem.get('v'))
            
            # Check house number
            # Check city
            for elem in element: 
                if elem.tag == 'tag' and re.match('addr:housenumber', elem.get('k')):
                    if not re.match(r'[0-9]+', elem.get('v')):
                        weird_numbers.append(elem.get('v'))
            
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
                    
    # Print audit results
    print('number of unique uids: ' + str(len(uids)))
    print('missing uids: ' + str(missing_uids))
    print('wrong ids: ' + str(wrong_ids))
    print('wrong timestamps: ' + str(wrong_timestamps))
    print('wrong longitude or latitude: ' + str(wrong_coords))
    print('ways with less than 2 node references: ' + str(wrong_ways))
    print('number of street abbreviations: ' + str(len(street_abreviations)))
    print(street_abreviations)
    print('number of unique tag names: ' + str(len(tags)))
    print('number of wrong postcodes: ' + str(len(wrong_postcodes)))
    if len(wrong_postcodes) < 50:    
        print(wrong_postcodes)
    else:
        print(wrong_postcodes[:50])
    print(cities)
    print('number of weird housenumbers: ' + str(len(weird_numbers)))
    print(weird_numbers)
    print('unexpected street names: ')
    print(weird_streets)


audit('interpreter.osm')


















