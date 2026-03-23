"""
Grid detection and YOLO-based object detection solver.
Handles grid sizing, YOLO model inference, and box-to-grid mapping.
"""
import cv2
import numpy as np
import streamlit as st


@st.cache_resource
def load_yolo_model():
    """Loads YOLOv8 model with caching for efficiency."""
    from ultralytics import YOLO  # pylint: disable=import-outside-toplevel
    return YOLO('yolov8n.pt')


def detect_grid_size(cleaned_image):
    """
    Detects grid size by finding square-like contours (cells).

    Args:
        cleaned_image: Preprocessed grayscale image

    Returns:
        int: Estimated grid size (3, 4, or 5)
    """
    thresh = cv2.adaptiveThreshold(cleaned_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    square_areas = []
    img_h, img_w = cleaned_image.shape
    total_area = img_h * img_w

    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4:
            _, _, w, h = cv2.boundingRect(approx)
            area = w * h
            aspect_ratio = float(w) / h
            if 0.7 < aspect_ratio < 1.3:
                if (total_area * 0.01) < area < (total_area * 0.25):
                    square_areas.append(area)

    if not square_areas:
        return 3

    avg_cell_area = np.median(square_areas)
    estimated_cells = total_area / avg_cell_area

    if 13 <= estimated_cells <= 22:
        return 4
    elif 6 <= estimated_cells <= 12:
        return 3
    elif 23 <= estimated_cells <= 30:
        return 5
    else:
        return 3


def detect_objects(image_pil, target_name, conf=0.25):
    """
    Uses YOLOv8 to find objects in the image.

    Args:
        image_pil: PIL Image object
        target_name: Name of object to detect
        conf: Confidence threshold (0.0 to 1.0)

    Returns:
        tuple: (YOLO result object, list of target bounding boxes)
    """
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
    """
    Maps bounding boxes to grid cell positions.

    Args:
        image_pil: PIL Image object
        target_boxes: List of bounding boxes [x_min, y_min, x_max, y_max]
        grid_size: Size of grid (e.g., 3, 4, 5)

    Returns:
        list: Sorted list of grid cell numbers (1-indexed)
    """
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

                if (x_min < c_x_max and x_max > c_x_min and
                        y_min < c_y_max and y_max > c_y_min):
                    squares.add(square_num)
                square_num += 1
    return sorted(list(squares))


def draw_visual_results(image_pil, grid_size, selected_squares):
    """
    Draws red grid and highlights target squares in green.

    Args:
        image_pil: PIL Image object
        grid_size: Size of grid
        selected_squares: List of grid cell numbers to highlight

    Returns:
        PIL Image with grid and highlights overlay
    """
    # Convert PIL to OpenCV format
    img = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
    h, w, _ = img.shape
    cell_w, cell_h = w / grid_size, h / grid_size

    # Create a copy for the transparent overlay
    overlay = img.copy()

    # 1. Draw the Red Grid lines
    for i in range(1, grid_size):
        # Vertical
        cv2.line(img, (int(i * cell_w), 0),
                 (int(i * cell_w), h), (0, 0, 255), 2)
        # Horizontal
        cv2.line(img, (0, int(i * cell_h)),
                 (w, int(i * cell_h)), (0, 0, 255), 2)

    # 2. Highlight selected squares in green
    square_num = 1
    for row in range(grid_size):
        for col in range(grid_size):
            if square_num in selected_squares:
                pt1 = (int(col * cell_w), int(row * cell_h))
                pt2 = (int((col + 1) * cell_w), int((row + 1) * cell_h))
                cv2.rectangle(overlay, pt1, pt2, (0, 255, 0), -1)
            square_num += 1

    # 3. Blend the images for transparency
    alpha = 0.35
    result_img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    # Convert back to RGB
    from PIL import Image  # pylint: disable=import-outside-toplevel
    return Image.fromarray(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
