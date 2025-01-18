import time
from PIL import Image
from PIL import ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions

"""
This file contains all functions necessary to controll the LED display
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

def drawImage(matrix: RGBMatrix, xsize: int, ysize: int, startpos: list[int]):
    """
    Draws a static rectangle of size xsize x ysize at the specified top-left
    coordinates on the given RGB matrix.

    Args:
        matrix (RGBMatrix): The RGB matrix on which to draw.
        xsize (int): The width of the rectangle.
        ysize (int): The height of the rectangle.
        startpos (list[int] or tuple[int, int]): [x, y] coordinates of the rectangle's
            top-left corner on the matrix.

    Raises:
        ValueError: If the provided matrix is not an instance of RGBMatrix, or if
            startpos is not a list/tuple of length 2.
    """
    if not isinstance(matrix, RGBMatrix):
        raise ValueError("Provided matrix must be an instance of RGBMatrix.")

    # Validate startpos
    if (not isinstance(startpos, (list, tuple))) or len(startpos) != 2:
        raise ValueError(
            "startpos must be a list or tuple of two integers, e.g., [x, y]."
        )

    startx, starty = startpos

    # Create an image buffer the size of the desired rectangle
    image = Image.new("RGB", (xsize, ysize))
    draw = ImageDraw.Draw(image)

    # Draw a rectangle across the entire image area
    draw.rectangle((0, 0, xsize - 1, ysize - 1), fill=(0, 0, 0), outline=(0, 0, 255))

    # Render this image at the specified position on the matrix
    matrix.SetImage(image, startx, starty)