"""
Main entry point for the LED Controller FastAPI application.
"""
import sys
import logging
from pathlib import Path

from fastapi import FastAPI
import uvicorn

from config import config
from endpoints import router
from api_key_auth import ApiKeyAuthMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add the custom library folder to sys.path
rgb_matrix_lib_path = Path(config.RGB_MATRIX_LIB_PATH)
if rgb_matrix_lib_path.exists() and str(rgb_matrix_lib_path) not in sys.path:
    sys.path.append(str(rgb_matrix_lib_path))
    logger.info(f"Added RGB matrix library path: {rgb_matrix_lib_path}")

# Create the FastAPI instance
app = FastAPI(
    title="LEDController",
    description="A Python-based service to control RGB LED Matrix via API",
    version="1.0.0"
)

# Add the API Key Auth middleware
app.add_middleware(ApiKeyAuthMiddleware)

# Include the router from endpoints.py
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Application startup event handler."""
    logger.info("LED Controller application starting up...")
    logger.info(f"Matrix configuration: {config.MATRIX_ROWS}x{config.MATRIX_COLS}")
    logger.info(f"Default brightness: {config.DEFAULT_BRIGHTNESS}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event handler."""
    logger.info("LED Controller application shutting down...")


if __name__ == "__main__":
    # Run the application using uvicorn
    logger.info(f"Starting server on {config.API_HOST}:{config.API_PORT}")
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
