from fastapi import APIRouter
import os
import time
import cv2
import numpy as np

# Internal module imports
import display

router = APIRouter()

@router.get("/hello")
async def sayHello():
    """
    This endpoint will return user info (IP, API key, currently used TIDAL login info etc.)
    """
    return {"message": "Hello from your async endpoint!"}

@router.post("/draw")
async def drawImage():
    """
    Test endpoint to draw an image to the matrix
    """
    brightness = 20
    options = display.setMatrixOptions(brightness)
    matrix = display.initializeMatrix(options)
    time.sleep(1)
    image_path = "/usr/LEDController/res/test.png"
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot identify image file {image_path}")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = display.scaleImage(image, 28)
    display.drawImage(matrix, image, [2, 2])
    time.sleep(10)
    matrix.Clear()
    return {"message": "success"}