# Import the FastAPI class to create the application instance
from fastapi import FastAPI
# Import the data router from the local routers module
from .routers.data_routes import router as data_router

# Initialize the FastAPI application with the title "Data Processing"
app = FastAPI(title="Data Processing")

# Include the data router to register the defined endpoints for data processing
app.include_router(data_router)