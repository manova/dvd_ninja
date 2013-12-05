from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector
from magnets.items import MagnetItem
from pymongo import MongoClient
import re

class MagnetSpider(BaseSpider):

	name = "magnet"
	other_urls = []
	names = []
	movies = MongoClient().movies.movies
	count = -1
	allowed_domains = [
	"kickass.to"
	]
	handle_httpstatus_list = [404,301]
	# rules = None

	def __init__(self, *args, **kwargs):
		super(MagnetSpider, self).__init__(*args, **kwargs)
		for i in self.movies.find({}, {'title':1, '_id':0}):
			title = i['title'].split(" (")[0]
			self.other_urls.append('http://kickass.to/search/' + title + '/?field=seeders&sorder=desc')
			self.names.append(title)
		self.rules = (Rule(SgmlLinkExtractor(), callback=self.parse, follow=True),)

	def start_requests(self):
		log.msg('Starting Crawl!', level=log.INFO)
		start_url = self.other_urls.pop(0)
		return [Request(start_url, meta={'items': []})]

	def parse(self, response):
		log.msg("Begin Magnet Parsing", level=log.INFO)
		log.msg("Response from: %s" % response.url, level=log.INFO)
		self.count+=1
		# print self.count
		print self.names[self.count].lower()
		hxs = Selector(response)
		entries = hxs.xpath('//tr[starts-with(@id,"torrent_")]')
		items=response.meta['items']
		db_entry = []
		for i in xrange(len(entries[:5])):
			# print "hey"
			item = MagnetItem()
			item['title'] = ''.join(entries[0].xpath('td[1]/div[2]/a[2]//text()').extract()).strip()
			# print 'title: ' + item['title']
			item['url'] = entries[i].xpath('td[1]/div[2]/a[2]/@href').extract()
			item['torrent'] = entries[i].xpath('td[1]/div[1]/a[starts-with(@title,"Download torrent file")]/@href').extract()
			item['magnet'] = entries[i].xpath('td[1]/div[1]/a[starts-with(@title,"Torrent magnet link")]/@href').extract()
			item['size'] = entries[i].xpath('td[2]/text()[1]').extract()
			item['sizeType'] = entries[i].xpath('td[2]/span/text()').extract()
			item['age'] = entries[i].xpath('td[4]/text()').extract()
			item['seed'] = entries[i].xpath('td[5]/text()').extract()
			item['leech'] = entries[i].xpath('td[6]/text()').extract()

			if self.names[self.count].lower() in item['title'].lower():
				log.msg("Item retrieved: %s" % item, level=log.INFO)
				db_entry.append({'torrent_link':item['torrent'][0], 'torrent_magnet':item['magnet'][0], 'torrent_title':item['title']})
				items.append(item)
		regex = re.compile('.*' + re.escape(self.names[self.count]) + '.*', re.IGNORECASE)
		self.movies.update({'title':{'$regex': regex}},{'$set':{'torrents':db_entry}})
		if self.other_urls:
			return Request(self.other_urls.pop(0), meta={'items': items}, dont_filter=True)
		return items

