from pymongo import MongoClient

MONGODB_URI = "localhost"
MONGODB_PORT = "27017"
MONGODB_DB_NAME = "music_recommendation"

GOOGLE_WORD2VEC_MODEL_PATH = "E:\\OneDrive - Politechnika Warszawska\\Studia\\semestr7\\MIR\\GoogleNews-vectors-negative300.bin"
MONGO_CLIENT = MongoClient(MONGODB_URI, int(MONGODB_PORT))