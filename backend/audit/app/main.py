# Import the FastAPI class to create the application instance
from fastapi import FastAPI
# Import the audit router from the local routers module
from .routers.audit_routes import router as audit_router

# Initialize the FastAPI application with the title "Audit"
app = FastAPI(title="Audit")

# Include the audit router to register the defined endpoints for log management
app.include_router(audit_router)