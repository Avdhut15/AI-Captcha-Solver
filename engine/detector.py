"""
Image preprocessing and utility functions for CAPTCHA solving.
Handles image cleaning and preparation for detection.
"""
import cv2
import numpy as np


def clean_captcha_image(image_pil):
    """
    The Digital Car Wash: Prepares the image for contour detection.

    Args:
        image_pil: PIL Image object

    Returns:
        Cleaned grayscale image for processing
    """
    img_array = np.array(image_pil)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    contrast = cv2.equalizeHist(gray)
    cleaned_img = cv2.bilateralFilter(contrast, 9, 75, 75)
    return cleaned_img
