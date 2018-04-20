import petitionspider
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy.utils.project import get_project_settings
import time

## crawler control
from pymongo import MongoClient

client = MongoClient()

db = client.petition
cllct = db.petition_count


surls = ['https://www1.president.go.kr/petitions/202136']

def spider_closing(spider):
    print("closing spider")
    
    
    settings = get_project_settings()
    crawler = Crawler(petitionspider.PetitionCountSpider,settings)
    global surls, cllct
    crawler.crawl(start_urls=surls,collection=cllct, petition_number = 202136)
    time.sleep(5)
    reactor.run()

dispatcher.connect(spider_closing, signal=signals.spider_closed)
settings = get_project_settings()
crawler = Crawler(petitionspider.PetitionCountSpider,settings)

# crawler.crawl(petitionspider.PetitionCountSpider,start_urls=surls,collection=cllct, petition_number = 205890)
crawler.crawl(start_urls=surls,collection=cllct, petition_number = 202136)

# process.crawl(petitionspider.PetitionCountSpider,start_urls=surls,collection=cllct, petition_number = 205890)
# process.start()

ll = reactor.run()

print("ll={}".format(ll))


