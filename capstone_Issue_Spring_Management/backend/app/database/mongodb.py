from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

database = client[os.getenv("DATABASE_NAME")]

users_collection = database["users"]