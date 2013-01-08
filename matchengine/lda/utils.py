import database
import config
import csv
import time


class dbDumper(object):
	'''
	Append the new posts to the corresponding raw JSON file.
	The ldacore.py will handle the data directly from the file,
	instead of interacting with db too much.
	'''
	def __init__(self):
		self._db_connector = database.Connection(\
			config.DB_HOST, config.DB_NAME, config.DB_USER, config.DB_PASSWORD)
		self._start_timestamp = -1 # default is fresh new.

	def __del__(self):
		self._db_connector.close()
	
	def set_start_timestamp(self, timestamp):
		self._start_timestamp = timestamp
	
	def dump_provides(self, tag, output_path):
		new_provides = self._db_connector.iter(
			'''select provide_id, provide_title, provide_content from provide 
			   where provide_pub_date > %s and tag = %s''', self._start_timestamp, tag)
		# append data to file.
		w = csv.writer(open(output_path, 'ab'), delimiter=',')
		try:
			for item in new_provides:
				w.writerow([item['provide_id'], item['provide_title'], item['provide_content']])
		except csv.Error as e:
			print e
	
	def dump_needs(self, tag, output_path):
		new_needs = self._db_connector.iter(
			'''select need_id, need_title, need_content from need
			   where need_pub_date > %s and tag = %s''', self._start_timestamp, tag)
		# append data to file.
		w = csv.writer(open(output_path, 'ab'), delimiter=',')
		try:
			for item in new_needs:
				w.writerow([item['need_id'], item['need_title'], item['need_content']])
		except csv.Error as e:
			print e


class MatchMerger(object):
	'''
	The match process is 2-pass: one initiates by provides while the other
	initiates by needs. This class is to merge the results come from the 
	two passes.
	'''

	def __init__(self):
		pass

	def merge_primary(self, primary_a, primary_b):
		#TODO: make merge faster in O(n).
		merge_table = {}
		key_pool = set(primary_a.keys()) | set(primary_b.keys()) # merge keys. O(nlogn).
		for key in key_pool:
			if key in primary_a.keys():
				match_a = set(primary_a[key])
			else:
				match_a = set()
			if key in primary_b.keys():
				match_b = set(primary_b[key])
			else:
				match_b = set()
			merge_table[key] = match_a | match_b
		
		return merge_table

	def merge_dual(self, dual_a, dual_b):
		#TODO: make merge faster in O(n).
		merge_table = {}
		key_pool = set(dual_a.keys()) | set(dual_b.keys())
		for key in key_pool:
			if key in dual_a.keys():
				match_a = set(dual_a[key])
			else:
				match_a = set()
			if key in dual_b.keys():
				match_b = set(dual_b[key])
			else:
				match_b = set()
			merge_table[key] = match_a | match_b
		
		return merge_table


class dbUpdater(object):
	'''
	Update the provide and need match tables to db, so that
	the future work is query the table.

	Note that it is for batch process, the online query still
	needs to use LDA online match.
	'''
	def __init__(self):
		self._db_connector = database.Connection(\
			config.DB_HOST, config.DB_NAME, config.DB_USER, config.DB_PASSWORD)

	def __del__(self):
		self._db_connector.close()
	
	def update_provide_match(self, match_table):
		ts = time.time()
		for provide_id in match_table.keys():
			for need_item in match_table[provide_id]:
				self._db_connector.execute('''
					insert into provide_match (provide_id, need_id, score, timestamp) 
					values (%s, %s, %s, %s) on duplicate key update score = %s, timestamp = %s''', 
					provide_id, need_item[0], need_item[1], ts, need_item[1], ts)

	def update_need_match(self, match_table):
		ts = time.time()
		for need_id in match_table:
			for provide_item in match_table[need_id]:
				self._db_connector.execute('''
				insert into need_match (need_id, provide_id, score, timestamp) values
				(%s, %s, %s, %s) on duplicate key update score = %s, timestamp = %s''', need_id,
				provide_item[0], provide_item[1], ts, provide_item[1], ts)


