'''
Initialize the tag service.
Load static tags into memory.
'''
#TODO: dynamic tag service.

from flask import Flask
from csv import reader
app = Flask(__name__)
app.config['Debug'] = 'True'

tags_dict = {}
STATIC_TAG_DIR = 'static_tag.csv'
rd = reader(open(STATIC_TAG_DIR, 'r'), delimiter=',')
for item in rd:
	if item[0] not in tags_dict.keys():
		tags_dict[item[0]] = []
	tags_dict[item[0]].append(item[1])

import views
