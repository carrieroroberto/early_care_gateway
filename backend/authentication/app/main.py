from fastapi import FastAPI
from .routers.authentication_routes import router as authentication_router

app = FastAPI(title="Authentication")

app.include_router(authentication_router)