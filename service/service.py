import sys
sys.path.append('..')

import petitionspider
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy.utils.project import get_project_settings
import time, threading

## crawler control
from pymongo import MongoClient



class crawler_thread(threading.Thread):
    def __init__(self,petition_num,mg_collection):
        super().__init__()
        print("inside init. petition_num={}".format(petition_num))
        self.petition_num = petition_num
        self.mg_collection = mg_collection
        print("init done. petition_num={} , mg_collection={}".format(self.petition_num,self.mg_collection))

    def run(self):
        dispatcher.connect(self.restart_crawler, signal=signals.spider_closed)
        settings = get_project_settings()
        crawler = Crawler(petitionspider.PetitionCountSpider,settings)
        crawler.crawl(start_urls=[self.get_setup_url()],collection=self.mg_collection, petition_number = self.petition_num)
        yields = reactor.run()
        print("yield from petnum={} : {}".format(self.petition_num,yields))

    def restart_crawler(self,spider):
        print("petnum={} calling restart_crawler".format(self.petition_num))
        petition_num = self.petition_num
        mg_collection = self.mg_collection
        settings = get_project_settings()
        crawler = Crawler(petitionspider.PetitionCountSpider,settings)
        url_list=[self.get_setup_url()]
        crawler.crawl(start_urls=url_list,collection=mg_collection, petition_number = petition_num)
        time.sleep(5)
        yields = reactor.run(installSignalHandlers=0)
        print("yield from petnum={} : {}".format(self.petition_num,yields))

    def get_setup_url(self):
        base_url = "https://www1.president.go.kr/petitions"
        return base_url+"/"+str(self.petition_num)


    



client = MongoClient()

db = client.petition
cllct = db.petition_count


READ_TARGET_FILE = "readlist.txt"

target_num=[]

def read_targets(target_file, target_list):
    
    fd = open(target_file,'r')

    lines = fd.read().splitlines()

    return_list = []
    
    
    for line in lines:
        print(line)
        conv = int(line)
        
        if conv not in return_list:
            return_list.append(conv) 
            
        else:
            print(conv, 'already included')

    
    
    return return_list
        


def launch_crawler(petition_num, mg_collection):
    print("launch_crawler petition_num={}".format(petition_num))
    t1 = crawler_thread(petition_num,mg_collection)
    print("thread for petnum={} created: {}".format(petition_num,t1))
    t1.start()


def launch_crawlers(target_list,mg_collection):
    print("target_list: ",target_list)
    for target in target_list:
        print("turn for ",target)
        launch_crawler(target,mg_collection)




def start_loop(target_file, target_list):
    parsed_targets =  read_targets(target_file,target_list)
    
    
    if not parsed_targets:
        print("empty targets")

    launch_crawlers(parsed_targets,cllct)







start_loop(READ_TARGET_FILE,target_num)



print("end of code")



# dispatcher.connect(spider_closing, signal=signals.spider_closed)
# settings = get_project_settings()
# crawler = Crawler(petitionspider.PetitionCountSpider,settings)

# # crawler.crawl(petitionspider.PetitionCountSpider,start_urls=surls,collection=cllct, petition_number = 205890)
# crawler.crawl(start_urls=surls,collection=cllct, petition_number = 202136)

# # process.start()

# ll = reactor.run()

# def spider_closing(spider):
#     print("closing spider")
    
    
#     settings = get_project_settings()
#     crawler = Crawler(petitionspider.PetitionCountSpider,settings)
#     global surls, cllct
#     crawler.crawl(start_urls=surls,collection=cllct, petition_number = 205890)
#     time.sleep(5)
#     reactor.run()

