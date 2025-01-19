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
    brightness = 40
    options = display.setMatrixOptions(brightness)
    matrix = display.initializeMatrix(options)
    time.sleep(1)
    imagePath = "/usr/LEDController/res/test.png"
    image = display.openImage(imagePath)
    image = display.scaleImage(image, 28)
    display.drawImage(matrix, image, [2,2])
    text = "Test string to scroll through"
    display.drawScrollText(matrix, text, [34,2])
    time.sleep(10)
    matrix.Clear()
    return {"message": "success"}