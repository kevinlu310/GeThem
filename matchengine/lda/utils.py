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
	
	def dump_provides(self):
		new_provides = self._db_connector.get(
			'''select provide_title, provide_content from provide 
			   where provide_pub_date > %s''' % self._start_timestamp)
		w = csv.writer(open(PROVIDES_DUMP_RAW_FILE, 'ab'), delimiter=',')
		for item in new_provides:
			w.writerow([item['provide_title'], item['provide_content']])
		w.close()
	
	def dump_needs(self):
		new_needs = self._db_connector.get(
			'''select need_title, need_content from need
			   where need_pub_date > %s''' % self._start_timestamp)
		w = csv.writer(open(NEEDS_DUMP_RAW_FILE, 'ab'), delimiter=',')
		for item in new_needs:
			w.writerow([item['need_title'], item['need_content']])
		w.close()


class dbUpdater(object):
	'''
	Update the provide_topic and need_topic table from the output
	of lda.
	'''
	def __init__(self):
		pass


