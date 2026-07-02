from pymongo import MongoClient

from app.core.config import settings

from app.core.logger import logger


client = MongoClient(settings.MONGO_URI)

database = client[settings.DATABASE_NAME]

logger.info("MongoDB Connected Successfully.")