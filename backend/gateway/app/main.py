from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.gateway_routes import router as gateway_router

app = FastAPI(title="Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gateway_router)