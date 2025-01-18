from fastapi import APIRouter
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
    display.drawImage(matrix)
    return {"message": "success"}