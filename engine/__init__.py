"""
Engine module for AI CAPTCHA Solver.
Provides modular components for solving different types of CAPTCHA challenges.
"""

from engine.captcha_engine import create_engine, CaptchaEngine
from engine.detector import clean_captcha_image
from engine.grid_solver import (
    detect_grid_size,
    detect_objects,
    map_boxes_to_grid,
    draw_visual_results,
    load_yolo_model
)
from engine.type_detector import detect_captcha_type

__all__ = [
    'create_engine',
    'CaptchaEngine',
    'clean_captcha_image',
    'detect_grid_size',
    'detect_objects',
    'map_boxes_to_grid',
    'draw_visual_results',
    'load_yolo_model',
    'detect_captcha_type'
]
