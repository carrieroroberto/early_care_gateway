from fastapi import FastAPI
from .routers.xai_routes import router as xai_router

app = FastAPI(title="Explainable AI")

app.include_router(xai_router)