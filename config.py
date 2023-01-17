from pymongo import MongoClient

MONGODB_URI = "localhost"
MONGODB_PORT = "27017"
MONGODB_DB_NAME = "music_recommendation"

MONGO_CLIENT = MongoClient(MONGODB_URI, int(MONGODB_PORT))