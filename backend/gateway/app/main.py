# Import necessary modules from FastAPI and the application's router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.gateway_routes import router as gateway_router

# Initialize the FastAPI application with a specific title for the Gateway service
app = FastAPI(title="Gateway")

# Configure Cross-Origin Resource Sharing (CORS) middleware
# This configuration allows requests from any origin ("*"), with any method and header
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the gateway router to register the endpoints defined in the routers module
app.include_router(gateway_router)