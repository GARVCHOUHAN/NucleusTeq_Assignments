import os
import sys
from pymongo import MongoClient
from app.core.config import settings
from app.core.logger import logger
from app.database.in_memory import InMemoryClient, InMemoryDatabase


if "pytest" in sys.modules or os.getenv("USE_IN_MEMORY_DB") == "true":
    client = InMemoryClient()
    database = InMemoryDatabase()
    logger.info("Using in-memory database for tests.")
else:
    client = MongoClient(
        settings.MONGO_URI,
        connect=False,
        serverSelectionTimeoutMS=5000
    )
    database = client[settings.DATABASE_NAME]
    logger.info("MongoDB client initialized.")
