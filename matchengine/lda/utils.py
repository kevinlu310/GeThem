import database
import csv

class dbDumper(object):
	'''
	Append the new posts to the corresponding raw JSON file.
	The ldacore.py will handle the data directly from the file,
	instead of interacting with db too much.
	'''
	def __init__(self, conn):
		self._db_connector = conn
		self._start_timestamp = -1 # default is fresh new.
	
	def set_start_timestamp(self, timestamp=-1):
		self._start_timestamp = timestamp
	
	def dump_provides(self, tag):
		new_provides = self._db_connector.get(
			'''select provide_id, provide_title, provide_content from provide 
			   where provide_pub_date > %s and tag = %s''' % (self._start_timestamp, tag))
		# append data to file.
		w = csv.writer(open(PROVIDES_DUMP_RAW_FILE + '_' + tag, 'ab'), delimiter=',')
		try:
			for item in new_provides:
				w.writerow([item['provide_title'], item['provide_content']])
		except csv.Error as e:
			print e
	
	def dump_needs(self, tag):
		new_needs = self._db_connector.get(
			'''select need_id, need_title, need_content from need
			   where need_pub_date > %s and tag = %s''' % (self._start_timestamp, tag))
		# append data to file.
		w = csv.writer(open(NEEDS_DUMP_RAW_FILE + '_' + tag, 'ab'), delimiter=',')
		try:
			for item in new_needs:
				w.writerow([item['need_title'], item['need_content']])
		except csv.Error as e:
			print e


class dbUpdater(object):
	'''
	Update the provide_topic and need_topic table from the output
	of lda.
	'''
	def __init__(self):
		pass


