from fastapi import FastAPI
from .routers.data_routes import router as data_router

app = FastAPI(title="Data Processing")

app.include_router(data_router)