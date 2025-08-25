"""
Configuration settings for the LED Controller application.
"""
import os
from pathlib import Path


class Config:
    """Application configuration class."""
    
    # API Configuration
    API_KEY = os.getenv("API_KEY")
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Matrix Configuration
    MATRIX_ROWS = int(os.getenv("MATRIX_ROWS", "32"))
    MATRIX_COLS = int(os.getenv("MATRIX_COLS", "64"))
    DEFAULT_BRIGHTNESS = int(os.getenv("DEFAULT_BRIGHTNESS", "40"))
    HARDWARE_MAPPING = os.getenv("HARDWARE_MAPPING", "adafruit-hat")
    
    # Path Configuration
    BASE_DIR = Path(__file__).parent
    FONTS_DIR = Path(os.getenv("FONTS_DIR", BASE_DIR / "fonts"))
    RESOURCES_DIR = Path(os.getenv("RESOURCES_DIR", BASE_DIR / "res"))
    DEFAULT_FONT_PATH = FONTS_DIR / "7x13.bdf"
    
    # RGB LED Matrix Library Path
    RGB_MATRIX_LIB_PATH = os.getenv(
        "RGB_MATRIX_LIB_PATH", 
        os.path.expanduser("~/rpi-rgb-led-matrix/bindings/python")
    )
    
    # Animation Configuration
    DEFAULT_SCROLL_SPEED = float(os.getenv("DEFAULT_SCROLL_SPEED", "0.05"))
    DEFAULT_OVERLAY_DURATION = float(os.getenv("DEFAULT_OVERLAY_DURATION", "20.0"))


# Global config instance
config = Config()