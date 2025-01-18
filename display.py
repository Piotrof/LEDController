import time
from PIL import Image
from PIL import ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions

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

def drawImage(matrix: RGBMatrix):
    """
    Draws an image with basic graphics primitives and scrolls it across the given RGB matrix.

    Args:
        matrix (RGBMatrix): The RGB matrix on which to draw and animate the image.

    Raises:
        ValueError: If the provided matrix is not an instance of RGBMatrix.
    """
    if not isinstance(matrix, RGBMatrix):
        raise ValueError("Provided matrix must be an instance of RGBMatrix.")

    # Create an image canvas (can be larger than the matrix if desired)
    image = Image.new("RGB", (32, 32))  # Adjust size as needed
    draw = ImageDraw.Draw(image)  # Create a drawing context

    # Draw shapes on the canvas
    draw.rectangle((0, 0, 31, 31), fill=(0, 0, 0), outline=(0, 0, 255))  # Blue outline
    draw.line((0, 0, 31, 31), fill=(255, 0, 0))  # Red diagonal line
    draw.line((0, 31, 31, 0), fill=(0, 255, 0))  # Green diagonal line

    # Scroll the image across the matrix
    for n in range(-32, 33):  # Scroll from top-left to bottom-right
        matrix.Clear()
        matrix.SetImage(image, n, n)  # Set image with offset
        time.sleep(0.05)  # Control animation speed

    time.sleep(5)
    matrix.Clear()
