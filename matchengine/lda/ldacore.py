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

'''
#TODO: Distribute each tag's workload to each machine, using HDFS.

import logging
import time
import csv
import numpy
import scipy
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
				for chunk in item[1:]: # item[0] is the global post id.
					line += ' ' + clear_punctuations(chunk)	
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
	dictionary.save('dictionary_' + str(time.time()) + '.dict')
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
			for chunk in item[1:]: # item[0] is the global post id.
				line += ' ' + clear_punctuations(chunk)
			documents.append(line)
	except csv.Error as e:
		print e
	logger.info('make_bow_corpus() has loaded all the dump file')

	# remove stop words and tokenize
	stop_words = set('for a of the and to in is'.split())
	texts = [[word for word in doc.lower().split() if word not in stop_words] for doc in documents]

	# create bag-of-words model.
	corpus = [dictionary.doc2bow(text) for text in texts]
	logger.info('make_bow_corpus() done')

	return {'global_id_keeper':global_id_keeper, 'bow_corpus':corpus}

def lda_train(corpus_struct, dictionary, num_topics=10):
	'''train the lda model'''
	lda_model = gensim.models.ldamodel.LdaModel(\
		corpus_struct['bow_corpus'], id2word=dictionary, num_topics=num_topics, update_every=0)
	lda_corpus = lda_model[corpus_struct['bow_corpus']]
	logger.info('lda_transform() finishes.')

	return lda_model

def lda_match(lda_model, corpus_struct, dictionary, dump_path):
	'''given both provides and needs, match them together under the same tag.'''
	# assign lda topic to primary post.
	primary_topic_assignment = []
	primary_id = corpus_struct['global_id_keeper']
	lda_corpus = lda_model[corpus_struct['bow_corpus']]
	for i in range(len(corpus_struct['global_id_keeper'])):
		topic = max(lda_corpus[i], key=lambda o: o[1])[0]
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
			for chunk in item[1:]
				line += ' ' + clear_punctuations(chunk)
			documents.append()
	except Error.csv as e:
		print e
	logger.info('lda_match() finishes loading dual documents')
	
	# remove stop words and tokenize
	stop_words = set('for a of the and to in is'.split())
	dual_texts = [[word for word in doc.lower().split() if word not in stop_words] for doc in documents]
	dual_bow_corpus = dictionary.doc2bow(dual_texts)
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
		primary_look_aside[parimary_topic_assignment[i]].append(primary_id[i])
	dual_look_aside = {}
	for i in range(len(dual_id)):
		if dual_topic_assignment[i] not in dual_look_aside:
			dual_look_aside[dual_topic_assignment[i]] = []
		dual_look_aside[dual_topic_assignment[i]].append(dual_id[i])
	logger.info('lda_match() creates the look aside tables')	
	
	# now match!
	primay_table = {}
	for i in range(len(primary_id)):
		primary_table[primary_id[i]] = dual_look_aside[primary_topic_assignment[i]]
	logger.info('lda_match() finishes primary match')
	
	dual_table = {}
	for i in range(len(dual_id)):
		dual_table[dual_id[i]] = primary_look_aside[dual_topic_assignment[i]]
	logger.info('lda_match() finishes dual match')

	return (primary_table, dual_table)
