from fastapi import FastAPI
from routers.authentication_routes import router as authentication_router

app = FastAPI()
app.include_router(authentication_router)