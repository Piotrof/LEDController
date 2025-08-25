"""
API endpoints for the LED Controller service.
"""
import logging
import time
from pathlib import Path

from fastapi import APIRouter, HTTPException

# Internal module imports
import display
from config import config

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/hello")
async def say_hello() -> dict:
    """
    Health check endpoint that returns a simple greeting.
    
    Returns:
        A dictionary with a greeting message.
    """
    logger.info("Health check endpoint accessed")
    return {"message": "Hello from your async endpoint!"}


@router.post("/draw")
async def draw_image() -> dict:
    """
    Test endpoint to draw the Tidal overlay.
    
    Returns:
        A dictionary indicating success or failure.
        
    Raises:
        HTTPException: If there's an error during image processing or display.
    """
    try:
        logger.info("Draw endpoint accessed")
        
        brightness = config.DEFAULT_BRIGHTNESS
        options = display.set_matrix_options(brightness)
        matrix = display.initialize_matrix(options)
        
        # Brief pause to ensure matrix is ready
        time.sleep(1)
        
        image_path = config.RESOURCES_DIR / "test.png"
        
        if not image_path.exists():
            logger.error(f"Test image not found at {image_path}")
            raise HTTPException(status_code=404, detail=f"Test image not found at {image_path}")
        
        image = display.open_image(str(image_path))
        image = display.scale_image(image, 28)
        text = "Test string to scroll through"
        
        display.draw_music_overlay(
            matrix, 
            text, 
            image, 
            (2, 20),  # start_pos_text
            (2, 2),   # start_pos_image
            20,       # duration
            0.2       # scroll_speed
        )
        
        matrix.Clear()
        logger.info("Draw operation completed successfully")
        return {"message": "success"}
        
    except Exception as e:
        logger.error(f"Error in draw endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")