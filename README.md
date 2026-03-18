# 🤖 Autonomous AI CAPTCHA Solver

An end-to-end, industry-level Machine Learning pipeline designed to autonomously solve grid-based image CAPTCHAs.

This project utilizes a **"Two-Brain Architecture"** to process intentionally obscured images, map geometric grids, and detect specific objects using state-of-the-art Deep Learning.

## ✨ Core Features

- **Digital "Car Wash" Preprocessing:** Utilizes OpenCV bilateral filtering and histogram equalization to strip adversarial noise and blur from CAPTCHA images.
- **Autonomous Grid Detection:** Mathematically calculates whether a CAPTCHA is a 3x3 or 4x4 grid using Canny Edge Detection and Hough Line Transforms.
- **Deep Learning Object Detection:** Integrates Ultralytics YOLOv8 (Nano) for high-speed, localized object recognition.
- **Coordinate Mapping:** Custom Python logic translates raw bounding-box pixel coordinates into actionable grid square numbers (e.g., "Click squares 1, 4, and 5").
- **Interactive Web UI:** Built with Streamlit for seamless, drag-and-drop user testing and real-time inference visualization.

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Computer Vision (Geometry & Preprocessing):** OpenCV, NumPy, Pillow
- **Deep Learning Engine:** PyTorch, Ultralytics (YOLOv8)

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Avdhut15/AI-Captcha-Solver.git](https://github.com/Avdhut15/AI-Captcha-Solver.git)
   cd AI-Captcha-Solver
   ```
2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the web application:**
   ```bash
   python -m streamlit run app.py
   ```
