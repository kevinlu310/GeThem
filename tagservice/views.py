from __future__ import with_statement
from flask import Flask
from flask import request
from flask import abort
from flask import Response
from tagservice import app
from tagservice import tags_dict
import simplejson as json

@app.route('/tags/<key>', methods=['GET', 'POST'])
def show_tags(key):
	if key == 'root':
		return json.dump(tags_dict.keys())
	if key not in tags_dict.keys():
		abort(404)
	return json.dump(tags_dict[key])
