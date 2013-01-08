#
# Copyrights (C) Gethem.com 2013
# Author: jilong.liao@gmail.com 
#

'''
This file is the core of the batch process of our match engine.

The topic model contains the following steps:
	- 1. obtain the new raw provide and need post.
	- 2. format the overall corpus and calculate TF-IDF model
		 for both provide and need.
	- 3. run LDA algorithm for provide and need
	- 4. Classify each need-to-provide.
	- 5. Classify each provide-to-need.

Note that the topic analysis is only within the same tag, so
we need to iterate the each tag.

The ready model information should be put into redis for
sharing and supporting online match.

'''
#TODO: Distribute each tag's workload to each machine, using HDFS.

import logging
import time
import csv
import math
import gensim
import config
import utils

# setup the logging.
logger = logging.getLogger('log.txt')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)

def clear_punctuations(post):
	post = post.replace('.', ' ')
	post = post.replace(',', ' ')
	post = post.replace('!', ' ')
	post = post.replace('?', ' ')
	post = post.replace('*', ' ')
	post = post.replace('-', ' ')
	post = post.replace('+', ' ')
	post = post.replace(':', ' ')
	return post

def make_dictionary(dump_dir_list):
	'''make the dictionary from all dump files.'''
	documents = []
	for dump_path in dump_dir_list:
		data_reader = csv.reader(open(dump_path, 'rb'), delimiter=',')
		try:
			for item in data_reader:
				line = ''
				for i in range(1, len(item)): # item[0] is the global post id.
					line += ' ' + clear_punctuations(item[i])	
				documents.append(line)
		except csv.Error as e:
			print e
	logger.info('make_dictionary() finishes loading documents')	
	
	# remove stop words and tokenize.
	stop_words = set('for a of the and to in is'.split())
	texts = [[word for word in doc.lower().split() if word not in stop_words] for doc in documents]
	logger.info('make_dictionary() finishes tokenization')

	# create dictionary.
	dictionary = gensim.corpora.Dictionary(texts)
	dictionary.save('dictionary_dump.dict')
	logger.info('make_dictionary() finishes dictionary generation')

	return dictionary

def make_bow_corpus(dump_path, dictionary):
	'''make bow corpus of a single tag's documents'''
	documents = []
	global_id_keeper = []
	data_reader = csv.reader(open(dump_path, 'rb'), delimiter=',')
	try:
		for item in data_reader:
			global_id_keeper.append(int(item[0]))
			line = ''
			for i in range(1, len(item)): # item[0] is the global post id.
				line += ' ' + clear_punctuations(item[i])
			documents.append(line)
	except csv.Error as e:
		print e
	logger.info('make_bow_corpus() has loaded all the dump file')

	# remove stop words and tokenize
	stop_words = set(config.NLP_STOP_WORDS.split())
	texts = [[word for word in doc.lower().split() if word not in stop_words] for doc in documents]

	# create bag-of-words model.
	corpus = [dictionary.doc2bow(text) for text in texts]
	logger.info('make_bow_corpus() done')

	return {'global_id_keeper':global_id_keeper, 'bow_corpus':corpus}

def lda_train(corpus_struct, dictionary, num_pass=20, num_topics=10, distributed=False,\
		chunksize=2000, alpha=None, eta=None, decay=0.5):
	'''train the lda model'''
	lda_model = gensim.models.ldamodel.LdaModel(\
		corpus_struct['bow_corpus'], id2word=dictionary, passes=num_pass, \
		num_topics=num_topics, update_every=0, distributed=distributed, \
		chunksize=chunksize, alpha=alpha, eta=eta, decay=decay)
	lda_corpus = lda_model[corpus_struct['bow_corpus']]
	logger.info('lda_transform() finishes.')

	return lda_model

def vector_similarity(vector_a, vector_b):
	'''calculate similarities between two vectors.'''
	norm_a = 0.0
	for i in range(len(vector_a)):
		norm_a += vector_a[i][1]**2
	norm_b = 0.0
	for i in range(len(vector_b)):
		norm_b += vector_b[i][1]**2
	
	dict_a = dict(vector_a)
	dict_b = dict(vector_b)
	intersect_keys = set(dict_a.keys()) & set(dict_b.keys())
	norm = 0.0
	for key in intersect_keys:
		norm += dict_a[key] * dict_b[key]
	return norm/math.sqrt(norm_a)/math.sqrt(norm_b)

def lda_match(lda_model, corpus_struct, dictionary, dump_path):
	'''given both provides and needs, match them together under the same tag.'''
	# assign lda topic to primary post.
	primary_topic_assignment = []
	primary_bow_corpus = corpus_struct['bow_corpus']
	primary_id = corpus_struct['global_id_keeper']
	for i in range(len(primary_id)):
		lda_topic = lda_model[primary_bow_corpus[i]]
		topic = max(lda_topic, key=lambda o: o[1])[0]
		primary_topic_assignment.append(topic)
	logger.info('lda_match() finishes the primary topic assignment')
	
	# handle dual documents.
	documents = []
	dual_id = []
	data_reader = csv.reader(open(dump_path, 'rb'), delimiter=',')
	try:
		for item in data_reader:
			dual_id.append(int(item[0]))
			line = ''
			for i in range(1, len(item)):
				line += ' ' + clear_punctuations(item[i])
			documents.append(line)
	except csv.Error as e:
		print e
	logger.info('lda_match() finishes loading dual documents')
	
	# remove stop words and tokenize
	stop_words = set(config.NLP_STOP_WORDS.split())
	dual_texts = [[word for word in doc.lower().split() if word not in stop_words] for doc in documents]
	dual_bow_corpus = [dictionary.doc2bow(text) for text in dual_texts]
	dual_topic_assignment = []
	for bow_doc in dual_bow_corpus:
		topic = max(lda_model[bow_doc], key=lambda o: o[1])[0]
		dual_topic_assignment.append(topic)
	logger.info('lda_match() finishes dual topic assignment')

	# create look aside table.
	primary_look_aside = {}
	for i in range(len(primary_id)):
		if primary_topic_assignment[i] not in primary_look_aside:
			primary_look_aside[primary_topic_assignment[i]] = []
		primary_look_aside[primary_topic_assignment[i]].append((i, primary_id[i]))
	dual_look_aside = {}
	for i in range(len(dual_id)):
		if dual_topic_assignment[i] not in dual_look_aside:
			dual_look_aside[dual_topic_assignment[i]] = []
		dual_look_aside[dual_topic_assignment[i]].append((i, dual_id[i]))
	logger.info('lda_match() creates the look aside tables')	
	
	# now match!
	primary_table = {}
	for i in range(len(primary_id)):
		primary_table[primary_id[i]] = []
		for dual_item in dual_look_aside[primary_topic_assignment[i]]:
			sim = vector_similarity(primary_bow_corpus[i], dual_bow_corpus[dual_item[0]])
			primary_table[primary_id[i]].append((dual_item[1], sim))
	logger.info('lda_match() finishes primary match')
	
	dual_table = {}
	for i in range(len(dual_id)):
		dual_table[dual_id[i]] = []
		for primary_item in primary_look_aside[dual_topic_assignment[i]]:
			sim = vector_similarity(dual_bow_corpus[i], primary_bow_corpus[primary_item[0]])
			dual_table[dual_id[i]].append((primary_item[1], sim))
	logger.info('lda_match() finishes dual match')

	return (primary_table, dual_table)

