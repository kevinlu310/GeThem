#
# This file is used to crawl the post from the craiglist.org.
# Especially the data in Knoxville, TN.
#

import os
import urllib2
import sys
import hashlib
import threading
import time
import Queue

class ccrawler(object):
	'''
		This class is to crawl the data in craiglist.org.
		Run in this way:
			ccrawler.run(arg1, arg2, arg3)
	'''

	def load_url(self, url_str):
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		data = ""
		try:
			r = opener.open(url_str)
			data = r.read()
			r.close()
		except:
			print "Exception: URL open failed." 
		return -1 if data == "" else data

	def get_next_link(self, content, pos=0):
		p = content.find('<p class=\"row\"', pos)
		p = content.find('<a href=', p)
		return (p, content[p+9:content.find('\"', p+10)])
	
	def get_next_index_url(self, content):
		if content == -1:
			return ""
		p = content.find('<p id=\"nextpage\"')
		p = content.find('<a href=', p+1)
		return p if p < 0 else content[p+9:content.find('\"', p+10)]
	
	def write_to_file(self, url, content, dpath):
		if not os.path.isdir(dpath):
			os.makedirs(dpath)
		try:
			f = open(dpath+hashlib.sha1(url).hexdigest()+'.html', 'w')
			f.write(content)
			f.close()
		except:
			print "\nError: cannot write file."
		return
		

class MyThread(threading.Thread):
	
	def __init__(self, url, dpath):
		threading.Thread.__init__(self)
		self._url = url
		self._dpath = dpath

	def run(self):
		c = ccrawler()
		q = Queue.Queue()
		e = threading.Event()

		page = -1
		cnt = 0
		while 1:
			
			# we must ensure the main page works!
			xurl = c.get_next_index_url(page)
			if xurl == -1: break

			page = c.load_url(self._url + xurl)
			if page == -1:
				e.wait(1)
				continue

			# get the page and record every post.
			p = 0
			while 1:
				if p >= 0:
					(p, link) = c.get_next_link(page, p+5)
					q.put(link)
				
				if q.empty(): break

				link = q.get()
				data = c.load_url(link)
				
				# failed then try it later.
				if data == -1: 
					q.put(link)
					continue

				c.write_to_file(link, data, self._dpath)
				print '.',
				e.wait(1)
			
			cnt += 1
			print
			print '==== Info ===='
			print 'Page: '+str(cnt)


		return

if __name__ == '__main__':
	parameter = [['http://knoxville.craigslist.org/ata/', os.getcwd() + '/data-repo/ata/'],
				['http://knoxville.craigslist.org/bar/', os.getcwd() + '/data-repo/bar/'],
				['http://knoxville.craigslist.org/bia/', os.getcwd() + '/data-repo/bia/'],
				['http://knoxville.craigslist.org/boo/', os.getcwd() + '/data-repo/boo/'],
				['http://knoxville.craigslist.org/bka/', os.getcwd() + '/data-repo/bka/'],
				['http://knoxville.craigslist.org/bfa/', os.getcwd() + '/data-repo/bfa/'],
				['http://knoxville.craigslist.org/sya/', os.getcwd() + '/data-repo/sya/'],
				['http://knoxville.craigslist.org/zip/', os.getcwd() + '/data-repo/zip/'],
				['http://knoxville.craigslist.org/fua/', os.getcwd() + '/data-repo/fua/'],
				['http://knoxville.craigslist.org/foa/', os.getcwd() + '/data-repo/foa/'],
				['http://knoxville.craigslist.org/jwa/', os.getcwd() + '/data-repo/jwa/'],
				['http://knoxville.craigslist.org/maa/', os.getcwd() + '/data-repo/maa/'],
				['http://knoxville.craigslist.org/rva/', os.getcwd() + '/data-repo/rva/'],
				['http://knoxville.craigslist.org/sga/', os.getcwd() + '/data-repo/sga/'],
				['http://knoxville.craigslist.org/tia/', os.getcwd() + '/data-repo/tia/'],
				['http://knoxville.craigslist.org/tla/', os.getcwd() + '/data-repo/tla/'],
				['http://knoxville.craigslist.org/wan/', os.getcwd() + '/data-repo/wan/'],
				['http://knoxville.craigslist.org/ara/', os.getcwd() + '/data-repo/ara/'],
				['http://knoxville.craigslist.org/pta/', os.getcwd() + '/data-repo/pta/'],
				['http://knoxville.craigslist.org/baa/', os.getcwd() + '/data-repo/baa/'],
				['http://knoxville.craigslist.org/haa/', os.getcwd() + '/data-repo/haa/'],
				['http://knoxville.craigslist.org/cta/', os.getcwd() + '/data-repo/cta/'],
				['http://knoxville.craigslist.org/ema/', os.getcwd() + '/data-repo/ema/'],
				['http://knoxville.craigslist.org/moa/', os.getcwd() + '/data-repo/moa/'],
				['http://knoxville.craigslist.org/cla/', os.getcwd() + '/data-repo/cla/'],
				['http://knoxville.craigslist.org/cba/', os.getcwd() + '/data-repo/cba/'],
				['http://knoxville.craigslist.org/ela/', os.getcwd() + '/data-repo/ela/'],
				['http://knoxville.craigslist.org/gra/', os.getcwd() + '/data-repo/gra/'],
				['http://knoxville.craigslist.org/gms/', os.getcwd() + '/data-repo/gms/'],
				['http://knoxville.craigslist.org/hsa/', os.getcwd() + '/data-repo/hsa/'],
				['http://knoxville.craigslist.org/mca/', os.getcwd() + '/data-repo/mca/'],
				['http://knoxville.craigslist.org/msa/', os.getcwd() + '/data-repo/msa/'],
				['http://knoxville.craigslist.org/pha/', os.getcwd() + '/data-repo/pha/'],
				['http://knoxville.craigslist.org/taa/', os.getcwd() + '/data-repo/taa/'],
				['http://knoxville.craigslist.org/vga/', os.getcwd() + '/data-repo/vga/']]
	
	for p in parameter:
		try:
			t = MyThread(p[0], p[1])
			t.setDaemon(True)
			t.start()
		except:
			print '\nError: cannot start new thread.'
	
	e = threading.Event()
	while 1:
		e.wait(1)
