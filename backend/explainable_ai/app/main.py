# Import the FastAPI class to create the application instance
from fastapi import FastAPI
# Import the XAI router from the local routers module
from .routers.xai_routes import router as xai_router

# Initialize the FastAPI application with the title "Explainable AI"
app = FastAPI(title="Explainable AI")

# Include the XAI router to register the defined endpoints for explainable AI services
app.include_router(xai_router)