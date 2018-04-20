import petitionspider
from scrapy.crawler import CrawlerProcess

from pymongo import MongoClient
import datetime
import pprint

# set up mongo db connection
client = MongoClient()

db = client.petition
cllct = db.petition_count


## crawler control
process = CrawlerProcess()

argss = {'petition_number',201953}
surls = ['https://www1.president.go.kr/petitions/201953']

argsb = {'start_urls':surls}

process.crawl(petitionspider.PetitionCountSpider,start_urls=surls,collection=cllct, petition_number = 201953)
process.start()






