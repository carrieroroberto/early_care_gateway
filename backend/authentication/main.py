from fastapi import FastAPI
from routers.authentication_routes import router as auth_router

app = FastAPI()
app.include_router(auth_router)