from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector
from magnets.items import MovieItem
from pymongo import MongoClient
import re

class MovieSpider(BaseSpider):

	name = "movie_info"
	other_urls = []
	names = []
	movies = MongoClient().movies.movies
	count = -1
	allowed_domains = [
	"rottentomatoes.com"
	]
	handle_httpstatus_list = [404]

	def __init__(self, *args, **kwargs):
		super(MovieSpider, self).__init__(*args, **kwargs)
		for i in self.movies.find({}, {'title':1, '_id':0}):
			title = i['title'].split(" (")[0]
			self.other_urls.append('http://www.rottentomatoes.com/search/?search=' + title)
			self.names.append(title)
		self.rules = (Rule(SgmlLinkExtractor(), callback=self.parse, follow=True),)

	def start_requests(self):
		log.msg('Starting Movie Info Crawl!', level=log.INFO)
		start_url = self.other_urls.pop(0)
		return [Request(start_url, meta={'items': []})]

	def parse(self, response):
		log.msg("Begin Parsing", level=log.INFO)
		log.msg("Response from: %s" % response.url, level=log.INFO)
		host = 'http://www.rottentomatoes.com'
		self.count+=1
		item = MovieItem()
		items = response.meta['items']
		print self.count
		print self.names[self.count].lower()
		hxs = Selector(response)
		name_path = hxs.xpath('//*[@id="movie_results_ul"]/li[1]/div[2]/h3/a/text()')
		if len(name_path)>0:
			name = name_path[0].extract()
			href = hxs.xpath('//*[@id="movie_results_ul"]/li[1]/div[2]/h3/a/@href')[0].extract()
			actor_paths = hxs.xpath('//*[@id="movie_results_ul"]/li[1]/div[2]/a/text()')
			actors = []
			for i in xrange(len(actor_paths)/2):
				actors.append(actor_paths[i].extract())
			item['title'] = name
			item['actors'] = actors
			return Request(host+href,
                      callback=self.parse_info, meta={'item':item, 'items':items}, dont_filter=True)
		if self.other_urls:
			return Request(self.other_urls.pop(0), meta={'items': items}, dont_filter=True)
		return items

	def parse_info(self, response):
		hxs = Selector(response)
		item = response.meta['item']
		items = response.meta['items']
		item['criticRating'] = hxs.xpath('//*[@id="all-critics-meter"]/text()')[0].extract()
		item['audienceRating'] = hxs.xpath('//*[@id="scorePanel"]/div/a/span/text()')[0].extract()

		regex = re.compile('.*' + re.escape(self.names[self.count]) + '.*', re.IGNORECASE)
		self.movies.update({'title':{'$regex': regex}}, {'$set':{'actors':item['actors'], 'critic_rating':item['criticRating'], 'audience_rating':item['audienceRating']}})
		log.msg("Parsed stage 2 url: "+response.url, level=log.INFO)
		items.append(item)
		if self.other_urls:
			return Request(self.other_urls.pop(0), meta={'items': items}, dont_filter=True)
		return items