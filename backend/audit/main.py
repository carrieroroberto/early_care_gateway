from fastapi import FastAPI
from routers.audit_routes import router as audit_router

app = FastAPI()
app.include_router(audit_router)