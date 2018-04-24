from crawler_thread import crawler_thread
from pymongo import MongoClient


# setup mongo client
client = MongoClient()

db = client.petition
cllct = db.petition_count



t1 = crawler_thread(207045,cllct)

t1.start()

t2= crawler_thread(205890,cllct)
t2.start()