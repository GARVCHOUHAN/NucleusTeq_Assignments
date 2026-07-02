from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.mongodb import client

from app.core.logger import logger


@asynccontextmanager
async def lifespan(application: FastAPI):

    logger.info(
        "Starting Issue & Sprint Management System..."
    )

    try:

        client.admin.command("ping")

        logger.info(
            "MongoDB Connected Successfully."
        )

    except Exception as exception:

        logger.error(
            f"MongoDB Connection Failed : {exception}"
        )

    yield

    logger.info(
        "Closing MongoDB Connection..."
    )

    client.close()

    logger.info(
        "Application Shutdown Complete."
    )