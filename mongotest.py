from pymongo import MongoClient
import datetime
import pprint

client = MongoClient()

db = client.petition
cllct = db.petition_count

# testitem = {'datetime': datetime.datetime.utcnow(), 'petition_num':47524,'petition_count':200}


# post_id  = collection.insert_one(testitem)



# print(post_id)

# pprint.pprint(collection.find_one({'petition_num':47524}))

cursor = cllct.find({})

for item in cursor:
    pprint.pprint(item)