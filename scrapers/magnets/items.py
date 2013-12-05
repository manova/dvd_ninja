from scrapy.item import Item, Field

class MagnetItem(Item):
 title = Field()
 url = Field()
 size = Field()
 sizeType = Field()
 age = Field()
 seed = Field()
 magnet = Field()
 leech = Field()
 torrent = Field()
pass

class MovieItem(Item):
 title = Field()
 criticRating = Field()
 audienceRating = Field()
 actors = Field()
 director = Field()
pass