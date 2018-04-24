import threading,time
from bs_crawler import PetitionCountCrawler

class crawler_thread(threading.Thread):
    def __init__(self,petition_num,mg_collection,period_sec=5):
        super().__init__()
        self.crawler = PetitionCountCrawler(petition_num)
        self.mg_collection = mg_collection
        if not period_sec>0:
            self.period_sec = 5
        else:
            self.period_sec = period_sec
    
    def run(self):
        self.crawler.fetch()
        self.loopfunction()

    def loopfunction(self):
        time.sleep(self.period_sec)
        self.crawler.fetch()
        self.loopfunction()

        
    