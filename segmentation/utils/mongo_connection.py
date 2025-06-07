from pymongo import MongoClient

# MongoDB URI and Database Name
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "ecommerce_db"

def get_mongo_client():
    """
    Returns a MongoClient connected to the hardcoded MongoDB instance.
    """
    return MongoClient(MONGO_URI)

def get_collection(collection_name):
    """
    Returns a collection object from the hardcoded database.
    """
    client = get_mongo_client()
    db = client[DB_NAME]
    return db[collection_name]
