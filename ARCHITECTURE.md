# AI CAPTCHA Solver - Refactored Architecture

## Project Structure

```
AICaptchaSolver/
├── app.py                    # Streamlit UI - Main interface
├── requirements.txt          # Project dependencies
├── yolov8n.pt              # YOLO model weights
├── README.md               # Project documentation
└── engine/                 # Core solver modules
    ├── __init__.py         # Package initialization
    ├── detector.py         # Image preprocessing utilities
    ├── grid_solver.py      # YOLO and grid-based detection
    ├── type_detector.py    # Captcha type classification
    ├── captcha_engine.py   # Main orchestration router
    ├── text_solver.py      # Text-based CAPTCHA solver (placeholder)
    └── math_solver.py      # Math-based CAPTCHA solver (placeholder)
```

## Module Responsibilities

### `detector.py` - Image Preprocessing

- **clean_captcha_image()**: Converts and enhances image for processing
  - RGB to grayscale conversion
  - Histogram equalization for contrast
  - Bilateral filtering for noise reduction

### `grid_solver.py` - Grid Detection & YOLO

- **load_yolo_model()**: Loads YOLOv8 model with Streamlit caching
- **detect_grid_size()**: Analyzes contours to estimate grid dimensions (3x3, 4x4, 5x5)
- **detect_objects()**: Uses YOLO to find target objects in image
- **map_boxes_to_grid()**: Converts bounding boxes to grid cell positions (1-indexed)
- **draw_visual_results()**: Creates visual overlay with red grid and green highlights

### `type_detector.py` - Captcha Classification

- **detect_captcha_type()**: Identifies captcha type (grid, text, math)
- **get_solver_for_type()**: Returns appropriate solver module for detected type
- Future: Add ML-based type classification

### `captcha_engine.py` - Main Router (Orchestration)

- **CaptchaEngine** class: Main solver orchestrator
- **solve()**: Unified entry point that:
  1. Detects captcha type
  2. Cleans image
  3. Detects grid size
  4. Runs YOLO detection
  5. Maps results to grid
  6. Generates visual output
  7. Returns structured results
- **create_engine()**: Factory function for creating engine instances

### `text_solver.py` - Text-Based Captcha (Placeholder)

- **solve_text_captcha()**: Main text solver entry point
- **preprocess_for_ocr()**: Image preparation for OCR
- **extract_text_with_ocr()**: OCR text extraction
- Status: Ready for implementing with Pytesseract or EasyOCR

### `math_solver.py` - Math-Based Captcha (Placeholder)

- **solve_math_captcha()**: Main math solver entry point
- **extract_math_expression()**: OCR for math expressions
- **evaluate_expression()**: Safe math expression evaluation
- Status: Ready for implementing OCR + expression parsing

### `app.py` - Streamlit UI

- Updated to use new `captcha_engine` module
- Simplified logic using `CaptchaEngine.solve()` method
- Maintains same user interface and functionality

## Data Flow

```
User Input (Image + Target Object)
        ↓
   [app.py]
        ↓
[captcha_engine.py]
        ↓
   ├─→ [type_detector.py] → Classify type
   ├─→ [detector.py] → Clean image
   ├─→ [grid_solver.py] → Detect grid, find objects
   └─→ Combine results
        ↓
Return Results (grid_size, solution cells, visual)
        ↓
   [app.py] → Display to user
```

## Key Improvements

✅ **Modularity**: Each solver is independent and replaceable
✅ **Clarity**: Clear responsibility separation
✅ **Extensibility**: Easy to add new solver types
✅ **Maintainability**: Focused, single-purpose modules
✅ **Testing**: Individual modules can be tested separately
✅ **Backward Compatibility**: Existing functionality unchanged

## Usage Example

```python
from engine.captcha_engine import create_engine
from PIL import Image

# Create engine
engine = create_engine()

# Load image
img = Image.open('captcha.png')

# Solve
result = engine.solve(img, target_object='bus', conf=0.25)

if result['success']:
    print(f"Found objects in cells: {result['solution']}")
    print(f"Grid size: {result['grid_size']}x{result['grid_size']}")
    result['visual'].show()
```

## Future Enhancements

1. **Text Solver**: Implement OCR-based text CAPTCHA solving
2. **Math Solver**: Implement math expression recognition and evaluation
3. **Type Detection**: Add ML-based automatic captcha type classification
4. **Caching**: Add solution caching for repeated CAPTCHA patterns
5. **API**: Create REST API wrapper for integration
6. **Batch Processing**: Support multiple images in sequence
7. **Confidence Estimation**: Return confidence scores for solutions
