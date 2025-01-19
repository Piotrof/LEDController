import time
import cv2
import numpy as np
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

def scaleImage(image, size):
    """
    Scales the image to the specified size.
    
    Args:
        image (numpy.ndarray): The image to be scaled.
        size (int): The size to scale the image to.
    
    Returns:
        numpy.ndarray: The scaled image.
    """
    return cv2.resize(image, (size, size))

def drawImage(matrix, image, startpos):
    """
    Draws the image on the matrix at the specified top-left coordinates.

    Args:
        matrix (RGBMatrix): The RGB matrix on which to draw.
        image (numpy.ndarray): The image to be drawn.
        startpos (list[int] or tuple[int, int]): [x, y] coordinates of the image's
            top-left corner on the matrix.

    Raises:
        ValueError: If the provided matrix is not an instance of RGBMatrix, if 'image'
            is not a numpy ndarray, or if 'startpos' is not a 2-element list/tuple.
    """
    # Validate matrix
    if not isinstance(matrix, RGBMatrix):
        raise ValueError("Provided matrix must be an instance of RGBMatrix.")

    # Validate image
    if not isinstance(image, np.ndarray):
        raise ValueError("Provided image must be a numpy ndarray.")

    # Validate startpos
    if not isinstance(startpos, (list, tuple)) or len(startpos) != 2:
        raise ValueError("startpos must be a list or tuple of length 2.")

    # Draw the image on the matrix
    x, y = startpos
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            matrix.SetPixel(x + j, y + i, int(image[i, j, 0]), int(image[i, j, 1]), int(image[i, j, 2]))