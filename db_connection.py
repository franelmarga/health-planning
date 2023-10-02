import pymongo

def establish_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["app"]
    collection = db["users"]
    return collection
