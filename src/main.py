import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.http.auth.create_session_controller import router as create_session_router
from src.adapters.http.auth.get_session_controller import router as get_session_router
from src.adapters.http.health_controller import router as health_router

isProd = True if os.getenv("ENV") == "production" else False
allowed_origins = ["https://www.everlastingvendetta.com"] if isProd else ["*"]
api_prefix = "/api/v1"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router( 
    prefix=f"",
    tags=["HealthController"],
    router=health_router
)

app.include_router(
    prefix=f"{api_prefix}/auth",
    tags=["AuthController"],
    router=create_session_router
)

app.include_router(
    prefix=f"{api_prefix}/auth",
    tags=["AuthController"],
    router=get_session_router
)