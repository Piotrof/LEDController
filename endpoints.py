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
    Test endpoint to draw the Tidal overlay
    """
    brightness = 40
    options = display.setMatrixOptions(brightness)
    matrix = display.initializeMatrix(options)
    time.sleep(1)
    imagePath = "/usr/LEDController/res/test.png"
    image = display.openImage(imagePath)
    image = display.scaleImage(image, 28)
    text = "Test string to scroll through"
    display.drawTidalOverlay(matrix,text,image,[32,20],[2,2],20,0.2)
    matrix.Clear()
    return {"message": "success"}