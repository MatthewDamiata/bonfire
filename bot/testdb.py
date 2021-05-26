import pprint
from pymongo import MongoClient
from tokens import *

def main():
    client = MongoClient("mongodb+srv://bonfire_app:"+DB_PASS+"@cluster0.ctzl1.mongodb.net/?retryWrites=true&w=majority")
    db = client.wyr
    col = db.positive
    #print(list(col.find())[0]['_id'])
    #print(list(col.find())[0]['option'])

    pipeline = [
        {"$project": {"option": 1, "_id": 1}},
        {"$sample": {"size": 2}},
    ]

    randomDocs = col.aggregate(pipeline)
    print(list(randomDocs))

if __name__ == '__main__':
    main()