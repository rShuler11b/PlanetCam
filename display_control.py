"""
Handles rendering images onto the Adafruit Mini PiTFT ST7789 display using the PIL library.
Manages display initialization and image rendering.
"""
from PIL import Image
import digitalio
import board
from adafruit_rgb_display import st7789

# Initialize display
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
display = st7789.ST7789(board.SPI(), cs=cs_pin, dc=dc_pin, rst=reset_pin, width=240, height=240)

def display_image(image_path):
    """Load and display an image on the TFT screen."""
    image = Image.open(image_path)
    display.image(image)
    print("Image displayed on screen")
