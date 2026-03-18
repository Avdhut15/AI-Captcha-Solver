"""
This module handles geometric contour detection for grid sizing 
and YOLOv8 for object recognition.
"""
import cv2
import numpy as np
import streamlit as st


def clean_captcha_image(image_pil):
    """The Digital Car Wash: Prepares the image for contour detection."""
    img_array = np.array(image_pil)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    # Equalize contrast to make the grid lines stand out from the background
    contrast = cv2.equalizeHist(gray)
    cleaned_img = cv2.bilateralFilter(contrast, 9, 75, 75)
    return cleaned_img


def detect_grid_size(cleaned_image):
    """
    Industry-Level: Detects grid size by finding square-like contours (cells).
    This ignores linear noise like power lines or crosswalks.
    """
    # 1. Create a binary 'map' of the image
    thresh = cv2.adaptiveThreshold(cleaned_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # 2. Find all closed shapes
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    square_areas = []
    img_h, img_w = cleaned_image.shape
    total_area = img_h * img_w

    for cnt in contours:
        # Check if the shape is roughly a rectangle
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

        # If it has 4 corners, it's a candidate for a grid cell
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            area = w * h
            aspect_ratio = float(w) / h

            # Filter: Cell must be square-ish (0.8 to 1.2 ratio)
            # and occupy a reasonable percentage of the total image
            if 0.7 < aspect_ratio < 1.3:
                if (total_area * 0.01) < area < (total_area * 0.25):
                    square_areas.append(area)

    # 3. Statistical Logic: If we found enough squares, calculate the grid
    if not square_areas:
        return 3  # Default to standard 3x3 if detection is too blurry

    avg_cell_area = np.median(square_areas)
    estimated_cells = total_area / avg_cell_area

    # Mapping the area ratio to the most likely grid dimension
    if 13 <= estimated_cells <= 22:
        return 4
    elif 6 <= estimated_cells <= 12:
        return 3
    elif 23 <= estimated_cells <= 30:
        return 5
    else:
        return 3


@st.cache_resource
def load_yolo_model():
    """Loads and caches the YOLOv8 Nano model."""
    from ultralytics import YOLO
    return YOLO('yolov8n.pt')


def detect_objects(image_pil, target_name, conf=0.25):
    """Brain 2: Uses YOLOv8 with user-defined confidence."""
    model = load_yolo_model()
    results = model.predict(source=image_pil, conf=conf, verbose=False)
    result = results[0]

    target_boxes = []
    for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
        class_name = model.names[int(cls)]
        if class_name.lower() == target_name.lower():
            target_boxes.append(box.tolist())

    return result, target_boxes


def map_boxes_to_grid(image_pil, target_boxes, grid_size):
    """Calculates grid cell numbers (1 to N) based on object coordinates."""
    width, height = image_pil.size
    cell_w, cell_h = width / grid_size, height / grid_size
    squares = set()

    for box in target_boxes:
        x_min, y_min, x_max, y_max = box
        square_num = 1
        for row in range(grid_size):
            for col in range(grid_size):
                c_x_min, c_y_min = col * cell_w, row * cell_h
                c_x_max, c_y_max = (col + 1) * cell_w, (row + 1) * cell_h

                # Check for overlap between the YOLO box and the grid cell
                if (x_min < c_x_max and x_max > c_x_min and
                        y_min < c_y_max and y_max > c_y_min):
                    squares.add(square_num)
                square_num += 1
    return sorted(list(squares))
