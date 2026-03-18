"""The main Streamlit web interface for the AI CAPTCHA Solver."""
import streamlit as st
from PIL import Image

# Import our custom AI engine (Both Brains + the Math Mapper)
from engine.detector import clean_captcha_image, detect_grid_size, detect_objects, map_boxes_to_grid

st.set_page_config(page_title="Autonomous CAPTCHA Solver", layout="centered")

st.title("🤖 Autonomous CAPTCHA Solver")
st.write("Upload a CAPTCHA screenshot. The AI will detect the grid size, find the target, and tell you which squares to click!")

target_object = st.text_input("What object are we looking for?", value="bus")
uploaded_file = st.file_uploader(
    "Upload your CAPTCHA Screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Original CAPTCHA", use_container_width=True)
    st.write("---")

    if st.button("🔍 Solve CAPTCHA", type="primary"):

        # --- BRAIN 1: THE ARCHITECT ---
        with st.spinner("Brain 1: Cleaning image and detecting grid..."):
            cleaned_img_matrix = clean_captcha_image(img)
            grid_size = detect_grid_size(cleaned_img_matrix)
            st.success(
                f"**Grid Detected!** The AI calculated this is a {grid_size}x{grid_size} grid.")

        # --- BRAIN 2: THE DETECTIVE ---
        with st.spinner(f"Brain 2: Unleashing YOLO to find '{target_object}'..."):
            yolo_result, boxes = detect_objects(img, target_object)

            if len(boxes) > 0:
                # --- NEW: TRANSLATING BOXES TO SQUARES ---
                squares_to_click = map_boxes_to_grid(img, boxes, grid_size)

                st.success(
                    f"**Target Found!** YOLO detected '{target_object}' in the image.")

                # Highlight the exact squares the user needs to click!
                st.markdown(
                    f"### 👉 **Click these squares: {squares_to_click}**")

                # Show the visual proof
                annotated_img = yolo_result.plot()
                st.image(annotated_img, caption="AI Vision: Bounding Boxes",
                         use_container_width=True, channels="BGR")
            else:
                st.warning(
                    f"YOLO couldn't find any '{target_object}'. Remember, this tiny YOLO only knows 80 basic words (like 'car', 'bus', 'person').")
