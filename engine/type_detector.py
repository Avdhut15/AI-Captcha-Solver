"""
Captcha type detection module.
Identifies the type of captcha challenge (grid-based, text-based, math-based, etc.).
"""


def detect_captcha_type(_image_pil):
    """
    Detects the type of captcha challenge.

    Args:
        _image_pil: PIL Image object

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
        return 'grid'
    elif captcha_type == 'text':
        return 'text'
    elif captcha_type == 'math':
        return 'math'
    else:
        return 'grid'  # Default fallback
