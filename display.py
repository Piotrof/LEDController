import time
import cv2
import numpy as np
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
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

def openImage(image_path: str):
    """
    Opens an image from the given path using OpenCV, converts it to RGB,
    and returns the resulting image array.

    Args:
        image_path (str): Path to the image file.

    Returns:
        numpy.ndarray: The image array in RGB format.

    Raises:
        ValueError: If the image cannot be opened.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot identify or open image file: {image_path}")

    # Convert the BGR image (default from OpenCV) to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb

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

def drawScrollText(matrix: RGBMatrix, text: str, startpos, fontPath: str = "/usr/LEDController/fonts/7x13.bdf"):
    """
    Continuously scrolls 'text' on the given 'matrix' starting at coordinates 'startpos' (x, y).
    This scroll repeats indefinitely until interrupted.

    Args:
        matrix (RGBMatrix): The RGB matrix on which to draw.
        text (str): The text to be displayed.
        startpos (list[int] or tuple[int, int]): [x, y] coordinates for the text's baseline
            on the matrix. (y is the vertical baseline for the font).
        font_path (str, optional): Path to a BDF font file. Defaults to a 7x13 BDF.

    Raises:
        ValueError: If matrix is not an instance of RGBMatrix or startpos is invalid.
    """
    if not isinstance(matrix, RGBMatrix):
        raise ValueError("Provided matrix must be an instance of RGBMatrix.")

    if not isinstance(startpos, (list, tuple)) or len(startpos) != 2:
        raise ValueError("startpos must be a list or tuple of length 2.")

    offscreen_canvas = matrix.CreateFrameCanvas()

    # Load font
    font = graphics.Font()
    font.LoadFont(fontpath)

    # Choose a text color (yellow here, can customize)
    text_color = graphics.Color(255, 255, 255)

    # Decompose startpos
    x_start, y_start = startpos

    # 'pos' is the current x-coordinate from which text is drawn.
    # Start it from the x_start offset plus the canvas width so it
    # scrolls in from the right side.
    pos = x_start + offscreen_canvas.width

    while True:
        offscreen_canvas.Clear()

        # DrawText returns the width of the drawn text in pixels
        text_length = graphics.DrawText(
            offscreen_canvas,
            font,
            pos,
            y_start,  # baseline for the font
            text_color,
            text
        )

        pos -= 1  # Move text left by 1 pixel each frame

        # Once the entire text has scrolled past the left boundary
        # (x_start + text_length < x_start), reset pos.
        # This means the text fully exits the screen, then we reset.
        if (pos + text_length < x_start):
            pos = x_start + offscreen_canvas.width

        time.sleep(0.05)  # Adjust scrolling speed
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

def drawTidalOverlay(matrix, text, image, startposText, startposImage, duration, scrollSpeed, fontPath: str = "/usr/LEDController/fonts/7x13.bdf"):
    """
    Draws an overlay with a static image and scrolling text on the matrix for a specified duration.

    Args:
        matrix (RGBMatrix): The RGB matrix on which to draw.
        text (str): The scrolling text to display.
        image (numpy.ndarray): The image to display.
        startpos_text (list[int] or tuple[int, int]): [x, y] coordinates for the text's baseline.
        startpos_image (list[int] or tuple[int, int]): [x, y] coordinates for the image's top-left corner.
        duration (float): The time in seconds for which the overlay should be drawn.
        font_path (str): Path to a BDF font file. Defaults to "/usr/LEDController/fonts/7x13.bdf".
    """
    # Prepare double buffer
    offscreenCanvas = matrix.CreateFrameCanvas()

    # Load font
    font = graphics.Font()
    font.LoadFont(fontPath)

    textColor = graphics.Color(255, 255, 255)

    # Unpack coordinates
    xTextStart, yTextStart = startposText
    xImgStart, yImgStart = startposImage

    # Start the text off-screen to the right
    pos = xTextStart + offscreenCanvas.width/2

    startTime = time.time()

    while True:
        # Check duration
        if time.time() - startTime >= duration:
            break

        offscreenCanvas.Clear()

        # 1) Draw the static image pixel-by-pixel
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                r, g, b = image[i, j]
                offscreenCanvas.SetPixel(
                    xImgStart + j,
                    yImgStart + i,
                    int(r), int(g), int(b)
                )

        # 2) Draw the scrolling text
        textLen = graphics.DrawText(
            offscreenCanvas,
            font,
            pos,
            yTextStart,
            textColor,
            text
        )

        # Move text left
        pos -= 1
        if (pos + textLen) <= 32:
            pos = xTextStart + offscreenCanvas.width

        # 3) Swap buffers to update display
        time.sleep(scrollSpeed)  # Adjust scrolling speed
        offscreenCanvas = matrix.SwapOnVSync(offscreenCanvas)