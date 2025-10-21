# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.api.routes import health, auth, users


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Trust only localhost by default; adjust when you deploy behind a domain/load balancer
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "*"])

# GZip for responses (threshold 1KB)
app.add_middleware(GZipMiddleware, minimum_size=1024)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # already a List[str]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)

# Optional: a simple root route
@app.get("/")
async def root():
    return {"name": settings.app_name, "status": "ok"}
