from fastapi import FastAPI
import uvicorn
from endpoints import router

# Import the custom middleware
from ApiKeyAuth import ApiKeyAuthMiddleware

# Create the FastAPI instance
app = FastAPI(title="LEDController")

# Add the API Key Auth middleware
app.add_middleware(ApiKeyAuthMiddleware)

# Include the router from endpoints.py
app.include_router(router)

if __name__ == "__main__":
    # Run the application using uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
