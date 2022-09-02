# initi mongodb
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
mongo = pymongo.MongoClient(f"{os.getenv('MongoClient')}", 25000)
db = mongo.templatedb
