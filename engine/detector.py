"""This module handles the image cleaning, grid detection, and object detection for the AI."""
import cv2
import numpy as np
import streamlit as st


def clean_captcha_image(image_pil):
    """The Digital Car Wash: Cleans the blurry CAPTCHA for the AI."""
    img_array = np.array(image_pil)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    contrast = cv2.equalizeHist(gray)
    cleaned_img = cv2.bilateralFilter(contrast, 9, 75, 75)
    return cleaned_img


def detect_grid_size(cleaned_image):
    """Analyzes the sharp lines to guess if it's a 3x3 or 4x4 grid."""
    edges = cv2.Canny(cleaned_image, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180,
                            threshold=100, minLineLength=100, maxLineGap=10)

    if lines is None:
        return 3
    # Adjusted the math slightly so it doesn't get confused by the white gaps!
    if len(lines) > 30:
        return 4
    else:
        return 3

# --- THE SPEED FIX: LAZY LOADING & CACHING ---


@st.cache_resource
def load_yolo_model():
    """Loads the heavy AI brain ONLY ONCE and keeps it in memory."""
    # We move the import inside here so the web page doesn't wait for it!
    from ultralytics import YOLO
    return YOLO('yolov8n.pt')


def detect_objects(image_pil, target_name):
    """Brain 2: Uses YOLO to find objects and returns their bounding boxes."""
    # Instantly grabs the model from memory instead of reloading it
    model = load_yolo_model()

    results = model.predict(source=image_pil, conf=0.25)
    result = results[0]

    target_boxes = []
    for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
        class_name = model.names[int(cls)]
        if class_name.lower() == target_name.lower():
            target_boxes.append(box.tolist())

    return result, target_boxes


def map_boxes_to_grid(image_pil, target_boxes, grid_size=3):
    """Calculates exactly which grid squares the YOLO boxes overlap with."""
    width, height = image_pil.size

    # Calculate the exact pixel size of a single grid cell
    cell_width = width / grid_size
    cell_height = height / grid_size

    squares_to_click = set()

    # Loop through every box YOLO found
    for box in target_boxes:
        x_min, y_min, x_max, y_max = box

        # Check every single square in the grid (1 through 9)
        square_number = 1
        for row in range(grid_size):
            for col in range(grid_size):
                # Calculate the boundaries of this specific grid square
                cell_x_min = col * cell_width
                cell_y_min = row * cell_height
                cell_x_max = (col + 1) * cell_width
                cell_y_max = (row + 1) * cell_height

                # OVERLAP MATH: Check if the YOLO box touches this grid square
                if (x_min < cell_x_max and x_max > cell_x_min and
                        y_min < cell_y_max and y_max > cell_y_min):

                    squares_to_click.add(square_number)

                square_number += 1

    # Return a neatly sorted list of the squares (e.g., [2, 3, 5])
    return sorted(list(squares_to_click))
