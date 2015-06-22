# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:02:51 2015

@author: juhosalminen1
"""

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.datascience

num_files = db.osm.find().count()
print('Number of items in db: ' + str(num_files))

example = db.osm.find_one({})
print(example)

