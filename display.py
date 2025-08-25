"""
This file contains all functions necessary to control the LED display and display elements.
"""
import time
import logging
from typing import Tuple, Union, List

import cv2
import numpy as np
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

from config import config

# Set up logging
logger = logging.getLogger(__name__)


def set_matrix_options(brightness: int) -> RGBMatrixOptions:
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
    options.rows = config.MATRIX_ROWS
    options.cols = config.MATRIX_COLS
    options.brightness = brightness
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = config.HARDWARE_MAPPING
    return options


def initialize_matrix(options: RGBMatrixOptions) -> RGBMatrix:
    """
    Initializes and returns an RGBMatrix instance using the provided RGBMatrixOptions.

    Args:
        options: The configuration options for the RGB matrix.

    Returns:
        The initialized RGB matrix.

    Raises:
        ValueError: If the options parameter is not an instance of RGBMatrixOptions.
    """
    if not isinstance(options, RGBMatrixOptions):
        raise ValueError("Provided options must be an instance of RGBMatrixOptions.")
    
    # Initialize the matrix with the provided options
    matrix = RGBMatrix(options=options)
    return matrix


def open_image(image_path: str) -> np.ndarray:
    """
    Opens an image from the given path using OpenCV, converts it to RGB,
    and returns the resulting image array.

    Args:
        image_path: Path to the image file.

    Returns:
        The image array in RGB format.

    Raises:
        ValueError: If the image cannot be opened.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot identify or open image file: {image_path}")

    # Convert the BGR image (default from OpenCV) to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb


def scale_image(image: np.ndarray, size: int) -> np.ndarray:
    """
    Scales the image to the specified size.
    
    Args:
        image: The image to be scaled.
        size: The size to scale the image to.
    
    Returns:
        The scaled image.
    """
    return cv2.resize(image, (size, size))


def draw_image(matrix: RGBMatrix, image: np.ndarray, start_pos: Tuple[int, int]) -> None:
    """
    Draws the image on the matrix at the specified top-left coordinates.

    Args:
        matrix: The RGB matrix on which to draw.
        image: The image to be drawn.
        start_pos: (x, y) coordinates of the image's top-left corner on the matrix.

    Raises:
        ValueError: If the provided matrix is not an instance of RGBMatrix, if 'image'
            is not a numpy ndarray, or if 'start_pos' is not a 2-element tuple.
    """
    # Validate matrix
    if not isinstance(matrix, RGBMatrix):
        raise ValueError("Provided matrix must be an instance of RGBMatrix.")

    # Validate image
    if not isinstance(image, np.ndarray):
        raise ValueError("Provided image must be a numpy ndarray.")

    # Validate start_pos
    if not isinstance(start_pos, (list, tuple)) or len(start_pos) != 2:
        raise ValueError("start_pos must be a list or tuple of length 2.")

    # Draw the image on the matrix
    x, y = start_pos
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            matrix.SetPixel(x + j, y + i, int(image[i, j, 0]), int(image[i, j, 1]), int(image[i, j, 2]))


def draw_scroll_text(
    matrix: RGBMatrix, 
    text: str, 
    start_pos: Tuple[int, int], 
    font_path: str = None
) -> None:
    """
    Continuously scrolls text on the given matrix starting at coordinates start_pos (x, y).
    This scroll repeats indefinitely until interrupted.

    Args:
        matrix: The RGB matrix on which to draw.
        text: The text to be displayed.
        start_pos: (x, y) coordinates for the text's baseline on the matrix. 
                  (y is the vertical baseline for the font).
        font_path: Path to a BDF font file. Defaults to configured default font.

    Raises:
        ValueError: If matrix is not an instance of RGBMatrix or start_pos is invalid.
    """
    if not isinstance(matrix, RGBMatrix):
        raise ValueError("Provided matrix must be an instance of RGBMatrix.")

    if not isinstance(start_pos, (list, tuple)) or len(start_pos) != 2:
        raise ValueError("start_pos must be a list or tuple of length 2.")
    
    if font_path is None:
        font_path = str(config.DEFAULT_FONT_PATH)

    offscreen_canvas = matrix.CreateFrameCanvas()

    # Load font
    font = graphics.Font()
    font.LoadFont(font_path)

    # Choose a text color (white)
    text_color = graphics.Color(255, 255, 255)

    # Decompose start_pos
    x_start, y_start = start_pos

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

        time.sleep(config.DEFAULT_SCROLL_SPEED)  # Adjust scrolling speed
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


def draw_music_overlay(
    matrix: RGBMatrix,
    text: str,
    image: np.ndarray,
    start_pos_text: Tuple[int, int],
    start_pos_image: Tuple[int, int],
    duration: float,
    scroll_speed: float,
    font_path: str = None
) -> None:
    """
    Draws an overlay with a static image and scrolling text on the matrix for a specified duration.

    Args:
        matrix: The RGB matrix on which to draw.
        text: The scrolling text to display.
        image: The image to display.
        start_pos_text: (x, y) coordinates for the text's baseline.
        start_pos_image: (x, y) coordinates for the image's top-left corner.
        duration: The time in seconds for which the overlay should be drawn.
        scroll_speed: Speed of text scrolling.
        font_path: Path to a BDF font file. Defaults to configured default font.
    """
    if font_path is None:
        font_path = str(config.DEFAULT_FONT_PATH)
    
    # Prepare double buffer
    offscreen_canvas = matrix.CreateFrameCanvas()

    # Load font
    font = graphics.Font()
    font.LoadFont(font_path)

    text_color = graphics.Color(255, 255, 255)

    # Unpack coordinates
    x_text_start, y_text_start = start_pos_text
    x_img_start, y_img_start = start_pos_image

    # Start the text off-screen to the right
    pos = x_text_start + offscreen_canvas.width // 2

    start_time = time.time()

    while True:
        # Check duration
        if time.time() - start_time >= duration:
            break

        offscreen_canvas.Clear()

        # 1) Draw the scrolling text
        text_len = graphics.DrawText(
            offscreen_canvas,
            font,
            pos,
            y_text_start,
            text_color,
            text
        )

        # 2) Draw a 2-pixel-wide black border around where the image will be drawn
        for i in range(-2, image.shape[0] + 2):
            for j in range(-2, image.shape[1] + 2):
                # Check if the current (i, j) position is outside the actual image boundaries
                if i < 0 or i >= image.shape[0] or j < 0 or j >= image.shape[1]:
                    offscreen_canvas.SetPixel(
                        x_img_start + j,
                        y_img_start + i,
                        0, 0, 0  # RGB black
                    )

        # 3) Draw the image
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                r, g, b = image[i, j]
                offscreen_canvas.SetPixel(
                    x_img_start + j,
                    y_img_start + i,
                    int(r), int(g), int(b)
                )

        # Move text left
        pos -= 1
        if (pos + text_len) <= 32:
            pos = x_text_start + offscreen_canvas.width

        # Swap buffers to update display
        time.sleep(scroll_speed)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)