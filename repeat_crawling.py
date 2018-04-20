import threading, time, subprocess
from pymongo import MongoClient
import petitionspider
from scrapy.crawler import CrawlerProcess


def launch_crawler(cpg):
    print("inside launch_crawler. cpg = {}".format(cpg))
    time.sleep(3)
    p = cpg.generate()
    p.start()
    threading.Thread(launch_crawler,args=(cpg,)).start()


class CrawlerProcessGenerator():
    petnum = 0
    surls = None
    process = CrawlerProcess()
    cllct = None

    def __init__(self,cllct, petnum):
        self.cllct = cllct
        self.petnum = petnum
        tempurl = "https://www1.president.go.kr/petitions/"+ str(self.petnum)
        self.surls = [tempurl]

    def generate(self):
        print("surls = {} \n petnum = {}".format(self.surls,self.petnum))
        process = CrawlerProcess()
        process.crawl(petitionspider.PetitionCountSpider,start_urls=self.surls,collection=self.cllct, petition_number = self.petnum)
        return process

# class myThread(threading.Thread):
#     def __init__(self,cfg):
#         self.cfg = cfg
    
#     def run(self):
#         print("inside run")
#         process = self.cfg.generate()
#         process.start()
#         time.sleep(5)
#         self.run()

def recursive():
    subprocess.call("python3 run_once.py",shell=True)
    time.sleep(5)
    recursive()



# setup generator

# crawlerprocessgenerator = CrawlerProcessGenerator(cllct, 201953)

# process = crawlerprocessgenerator.generate()

# print(process)

# launch_crawler(crawlerprocessgenerator)

# thread = myThread(crawlerprocessgenerator)

# thread.run()

recursive()