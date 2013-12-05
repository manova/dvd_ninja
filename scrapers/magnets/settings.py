# Scrapy settings for magnets project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'magnets'

SPIDER_MODULES = ['magnets.spiders']
NEWSPIDER_MODULE = 'magnets.spiders'
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'magnets (+http://www.yourdomain.com)'
