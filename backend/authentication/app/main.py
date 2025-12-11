# Import FastAPI to create the application instance
from fastapi import FastAPI
# Import the authentication router from the local routers module
from .routers.authentication_routes import router as authentication_router

# Initialize the FastAPI app with the title "Authentication"
app = FastAPI(title="Authentication")

# Include the authentication router to register the defined endpoints
app.include_router(authentication_router)