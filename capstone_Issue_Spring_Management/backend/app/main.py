from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.health_router import router as health_router

from app.core.lifespan import lifespan


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