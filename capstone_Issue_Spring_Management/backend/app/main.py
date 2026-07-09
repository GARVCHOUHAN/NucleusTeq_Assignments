from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.api.auth_router import router as auth_router
from app.api.health_router import router as health_router

from app.core.lifespan import lifespan
from app.exceptions.handlers import register_exception_handlers

from app.api.project_router import (router as project_router)
from app.api.issue_router import (router as issue_router)
from app.api.sprint_router import router as sprint_router
from app.api.comment_router import router as comment_router
from app.api.dashboard_router import router as dashboard_router

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

application.include_router(
    issue_router
)

application.include_router(
    sprint_router
)

application.include_router(
    comment_router
)

application.include_router(
    dashboard_router
)

register_exception_handlers(application)

