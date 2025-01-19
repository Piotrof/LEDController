import time
from PIL import Image
from PIL import ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import os

"""
This file contains all functions necessary to controll the LED display and display ellements.
"""

def setMatrixOptions(brightness: int):
    """
    Creates and returns a configured RGBMatrixOptions object.

    Args:
        brightness (int): Brightness level (0-100).

    Returns:
        RGBMatrixOptions: Configured matrix options.

    Raises:
        ValueError: If brightness is not between 0 and 100.
    """
    if not (0 <= brightness <= 100):
        raise ValueError("Brightness must be between 0 and 100.")
    
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.brightness = brightness
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'  # For Adafruit HAT
    return options

def initializeMatrix(options: RGBMatrixOptions) -> RGBMatrix:
    """
    Initializes and returns an RGBMatrix instance using the provided RGBMatrixOptions.

    Args:
        options (RGBMatrixOptions): The configuration options for the RGB matrix.

    Returns:
        RGBMatrix: The initialized RGB matrix.

    Raises:
        ValueError: If the options parameter is not an instance of RGBMatrixOptions.
    """
    if not isinstance(options, RGBMatrixOptions):
        raise ValueError("Provided options must be an instance of RGBMatrixOptions.")
    
    # Initialize the matrix with the provided options
    matrix = RGBMatrix(options=options)
    return matrix

def openImage(image_path: str) -> Image.Image:
    """
    Opens and returns a PIL Image object from the specified file path.

    Args:
        image_path (str): The path to the image file.

    Returns:
        PIL.Image.Image: The opened image.

    Raises:
        ValueError: If the provided image_path is not a valid file path.
    """
    if not os.path.isfile(image_path):
        raise ValueError("Invalid image file path provided.")
    
    image = Image.open(image_path)
    image = image.convert("RGB")
    return image

def drawImage(matrix: RGBMatrix, image: Image.Image, startpos: list[int]):
    """
    Draws the provided PIL Image pixel-by-pixel on the given RGB matrix at the
    specified top-left coordinates.

    Args:
        matrix (RGBMatrix): The RGB matrix on which to draw.
        image (PIL.Image.Image): The PIL Image to be drawn.
        startpos (list[int] or tuple[int, int]): [x, y] coordinates of the image's
            top-left corner on the matrix.

    Raises:
        ValueError: If the provided matrix is not an instance of RGBMatrix, if 'image'
            is not a PIL Image, or if 'startpos' is not a 2-element list/tuple.
    """
    # Validate matrix
    if not isinstance(matrix, RGBMatrix):
        raise ValueError("Provided matrix must be an instance of RGBMatrix.")

    # Validate image
    if not isinstance(image, Image.Image):
        raise ValueError("Provided image must be a PIL Image object.")

    # Validate startpos
    if not isinstance(startpos, (list, tuple)) or len(startpos) != 2:
        raise ValueError("startpos must be a list or tuple of two integers, e.g., [x, y].")

    startx, starty = startpos

    # Get image dimensions
    width, height = image.size

    # Draw each pixel to the matrix
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            matrix.SetPixel(startx + x, starty + y, r, g, b)

def scaleImage(image: Image.Image, new_size: int) -> Image.Image:
    """
    Scales the given PIL Image to new_size x new_size pixels and returns the resized image.
    
    Args:
        image (PIL.Image.Image): The input image to scale.
        new_size (int): The width and height (in pixels) to which the image should be scaled.
    
    Returns:
        PIL.Image.Image: A new Image object resized to new_size x new_size pixels.
    """
    # Use a high-quality resampling filter such as LANCZOS
    resized_image = image.resize((new_size, new_size), resample=Image.Resampling.LANCZOS)
    return resized_image