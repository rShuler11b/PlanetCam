"""
Handles GPIO button inputs for starting/stopping the camera feed and capturing images.
Uses RPi.GPIO for handling button press events with debounce logic.
"""
import RPi.GPIO as GPIO
import time
from config import BUTTON_FEED, BUTTON_CAPTURE

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_FEED, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_CAPTURE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def is_button_pressed(button_pin):
    """Check if a button is pressed."""
    return GPIO.input(button_pin) == GPIO.LOW

def wait_for_button_release(button_pin):
    """Debounce button press."""
    time.sleep(0.5)  # Prevent accidental multiple triggers

