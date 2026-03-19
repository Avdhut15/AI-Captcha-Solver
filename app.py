"""The professional Streamlit interface with Visual Overlay support."""
import streamlit as st
from PIL import Image
from engine.detector import (
    clean_captcha_image,
    detect_grid_size,
    detect_objects,
    map_boxes_to_grid,
    draw_visual_results
)

st.set_page_config(page_title="AI CAPTCHA Solver", layout="wide")

st.title("🤖 Autonomous AI CAPTCHA Solver")
st.markdown("---")

# --- SIDEBAR ---
st.sidebar.header("🛠️ Configuration")
target_object = st.sidebar.text_input("Object to Find:", value="bus")
conf_val = st.sidebar.slider("AI Confidence", 0.05, 1.0, 0.25)
manual_grid = st.sidebar.number_input(
    "Manual Grid Size (0=Auto)", min_value=0, max_value=6, value=0)

st.sidebar.write("---")
st.sidebar.info(
    "The visual overlay helps you confirm if the AI is 'thinking' correctly about the grid.")

# --- MAIN INTERFACE ---
uploaded_file = st.file_uploader(
    "Upload CAPTCHA Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption="Input Screenshot", use_container_width=True)

    if st.button("🚀 Run AI Solver", type="primary"):
        with st.spinner("Analyzing..."):
            # 1. Image Cleaning
            cleaned = clean_captcha_image(img)

            # 2. Grid logic
            auto_size = detect_grid_size(cleaned)
            grid_size = manual_grid if manual_grid > 0 else auto_size

            # 3. Detection
            yolo_result, boxes = detect_objects(
                img, target_object, conf=conf_val)

            with col2:
                if len(boxes) > 0:
                    squares = map_boxes_to_grid(img, boxes, grid_size)

                    # 4. Generate Visual Overlay
                    visual_img = draw_visual_results(img, grid_size, squares)

                    st.success(f"Grid: {grid_size}x{grid_size}")
                    st.markdown(f"### 👉 **Click Squares: {squares}**")

                    # Show the Result Image
                    st.image(
                        visual_img, caption="AI Solution (Grid + Highlights)", use_container_width=True)
                else:
                    st.error(f"AI could not find any '{target_object}'.")
                    st.info("Try lowering the Confidence slider in the sidebar.")
