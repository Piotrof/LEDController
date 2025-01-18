from fastapi import APIRouter
import time
from PIL import Image

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
    image = Image.open("res/tea_sample.jpg")
    image = image.conver("RGB")
    image = display.scaleImage(image, 28)
    display.drawImage(matrix,image,[2,2])
    time.sleep(10)
    matrix.Clear()
    return {"message": "success"}