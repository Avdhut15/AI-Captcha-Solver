"""
Main CAPTCHA solver engine.
Routes requests to appropriate solvers based on captcha type.
Coordinates image preprocessing, detection, and result delivery.
"""

from engine.detector import clean_captcha_image
from engine.grid_solver import (
    detect_grid_size,
    detect_objects,
    map_boxes_to_grid,
    draw_visual_results
)
from engine.type_detector import detect_captcha_type


class CaptchaEngine:
    """Main router for CAPTCHA solving."""

    def __init__(self):
        """Initialize the CAPTCHA engine."""
        self.captcha_type = None
        self.grid_size = None
        self.target_boxes = []
        self.solution = []

    def solve(self, image_pil, target_object, conf=0.25, manual_grid=None):
        """
        Solve a CAPTCHA challenge.

        Args:
            image_pil: PIL Image object
            target_object: Name of object to find
            conf: Confidence threshold for object detection
            manual_grid: Optional manual grid size override

        Returns:
            dict: Solution result with keys:
                - 'success': bool
                - 'grid_size': int
                - 'solution': list of grid cells to click
                - 'message': str description
                - 'visual': PIL Image with grid overlay
        """
        result = {
            'success': False,
            'grid_size': None,
            'solution': [],
            'message': '',
            'visual': None
        }

        try:
            # 1. Detect captcha type
            self.captcha_type = detect_captcha_type(image_pil)

            # 2. Preprocess image
            cleaned = clean_captcha_image(image_pil)

            # 3. Detect grid size (auto or manual)
            auto_grid = detect_grid_size(cleaned)
            self.grid_size = manual_grid if manual_grid and manual_grid > 0 else auto_grid

            # 4. Detect objects
            _, self.target_boxes = detect_objects(
                image_pil, target_object, conf=conf
            )

            # 5. Map boxes to grid
            if len(self.target_boxes) > 0:
                self.solution = map_boxes_to_grid(
                    image_pil, self.target_boxes, self.grid_size
                )

                # 6. Generate visual overlay
                visual_img = draw_visual_results(
                    image_pil, self.grid_size, self.solution
                )

                result['success'] = True
                result['grid_size'] = self.grid_size
                result['solution'] = self.solution
                result['message'] = f"Found {len(self.solution)} objects in {self.grid_size}x{self.grid_size} grid"
                result['visual'] = visual_img
            else:
                result['message'] = f"No '{target_object}' objects detected. Try lowering confidence."
                result['visual'] = image_pil

        except Exception as error:  # pylint: disable=broad-except
            result['message'] = f"Error during solving: {str(error)}"
            result['visual'] = image_pil

        return result


def create_engine():
    """Factory function to create a new CAPTCHA engine instance."""
    return CaptchaEngine()
