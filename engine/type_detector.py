"""
Captcha type detection module.
Identifies the type of captcha challenge (grid-based, text-based, math-based, etc.).
"""


def detect_captcha_type(image_pil):
    """
    Detects the type of captcha challenge.

    Args:
        image_pil: PIL Image object

    Returns:
        str: Type of captcha ('grid', 'text', 'math', 'unknown')
    """
    # Placeholder: Currently defaults to grid-based detection
    # Future: Add logic to analyze image characteristics
    # - OCR-based detection for text vs objects
    # - Pattern recognition for math captchas
    # - Structural analysis for different layouts

    return 'grid'


def get_solver_for_type(captcha_type):
    """
    Returns the appropriate solver module for the detected captcha type.

    Args:
        captcha_type: str, type of captcha

    Returns:
        module: The solver module to use
    """
    if captcha_type == 'grid':
        from engine.grid_solver import detect_grid_size, detect_objects, map_boxes_to_grid
        return 'grid'
    elif captcha_type == 'text':
        from engine.text_solver import solve_text_captcha
        return 'text'
    elif captcha_type == 'math':
        from engine.math_solver import solve_math_captcha
        return 'math'
    else:
        return 'grid'  # Default fallback
