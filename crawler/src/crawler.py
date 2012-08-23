#
# This file is used to crawl the post from the craiglist.org.
# Especially the data in Knoxville, TN.
#

import os
import urllib2
import sys
import hashlib

class ccrawler(object):
	'''
		This class is to crawl the data in craiglist.org.
		Run in this way:
			ccrawler.run(arg1, arg2, arg3)
	'''

	def load_url(self, url_str):
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		r = opener.open(url_str)
		return r.read()

	def get_next_link(self, content, pos=0):
		p = content.find('<p class=\"row\"', pos)
		p = content.find('<a href=', p)
		return (p, content[p+9:content.find('\"', p+10)])
	
	def get_next_index_url(self, content):
		p = content.find('<p id=\"nextpage\"')
		p = content.find('<a href=', p+1)
		return p if p < 0 else content[p+9:content.find('\"', p+10)]
	
	def write_to_file(self, url, content, dpath):
		if not os.path.isdir(dpath):
			os.makedirs(dpath)
		f = open(dpath+hashlib.sha1(url).hexdigest()+'.html', 'w')
		f.write(content)
		f.close()
		return

	def run(self, url_str, dpath):
		page = self.load_url(url_str)
		cnt = 0
		while (True):
			p = 0
			while (True):
				(p, link) = self.get_next_link(page, p+5)
				if p < 0: break
				data = self.load_url(link)
				self.write_to_file(link, data, dpath)
				print '.',
			
			cnt += 1
			print '==== Info ===='
			print 'Page: '+str(cnt)
			page = self.load_url(url_str+self.get_next_index_url(page))

		return


if __name__ == '__main__':
	c = ccrawler()
	c.run('http://knoxville.craigslist.org/ppa/', os.getcwd() + '/craigslist/ppa/')

