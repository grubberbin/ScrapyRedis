from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", 'crawl', 'movie'])
# execute(["scrapy", 'crawl', 'movie_crawlspider'])
