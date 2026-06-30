from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.api.auth_router import router as auth_router
from app.api.health_router import router as health_router

from app.core.lifespan import lifespan
from app.exceptions.handlers import register_exception_handlers

from app.routers.project_router import (router as project_router)

application = FastAPI(

    title="Issue & Sprint Management System",

    version="1.0.0",

    lifespan=lifespan

)

application.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

application.include_router(
    health_router
)


application.include_router(
    auth_router
)

application.include_router(
    project_router
)

register_exception_handlers(application)