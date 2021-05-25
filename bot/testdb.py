import pprint
from pymongo import MongoClient
from tokens import *

def main():
    client = MongoClient("mongodb+srv://bonfire_app:"+DB_PASS+"@cluster0.ctzl1.mongodb.net/?retryWrites=true&w=majority")
    db = client.wyr
    col = db.positive
    print(list(col.find())[0]['_id'])
    print(list(col.find())[0]['option'])

if __name__ == '__main__':
    main()