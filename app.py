"""The professional Streamlit interface for the AI CAPTCHA Solver."""
import streamlit as st
from PIL import Image
from engine.detector import clean_captcha_image, detect_grid_size, detect_objects, map_boxes_to_grid

st.set_page_config(page_title="Autonomous AI Solver", layout="wide")

st.title("🤖 Autonomous CAPTCHA Solver")
st.markdown("---")

# --- SIDEBAR: The Control Room ---
st.sidebar.header("🛠️ AI Configuration")
target_object = st.sidebar.text_input("Find Object:", value="bus")
conf_val = st.sidebar.slider("AI Confidence Threshold", 0.05, 1.0, 0.25)
manual_grid = st.sidebar.number_input(
    "Override Grid Size (0 = Auto)", min_value=0, max_value=6, value=0)

st.sidebar.write("---")
st.sidebar.info(
    "💡 **Pro Tip:** If the AI misses a blurry object, lower the Confidence Threshold. If it detects the wrong grid size, use the Override.")

# --- MAIN PAGE: The Inference Zone ---
uploaded_file = st.file_uploader(
    "Upload CAPTCHA Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption="Uploaded Image", use_container_width=True)

    if st.button("🚀 Run AI Solver", type="primary"):
        with st.spinner("Executing Computer Vision Pipeline..."):
            # 1. Image Washing
            cleaned = clean_captcha_image(img)

            # 2. Grid Estimation
            auto_size = detect_grid_size(cleaned)
            grid_size = manual_grid if manual_grid > 0 else auto_size

            # 3. Target Detection
            yolo_result, boxes = detect_objects(
                img, target_object, conf=conf_val)

            with col2:
                if len(boxes) > 0:
                    # 4. Result Mapping
                    squares = map_boxes_to_grid(img, boxes, grid_size)

                    st.success(f"**Grid Detected:** {grid_size}x{grid_size}")
                    st.markdown(f"### 👉 **Click Squares: {squares}**")

                    # 5. Result Visualization
                    annotated_img = yolo_result.plot()
                    st.image(annotated_img, caption="AI Vision Results",
                             use_container_width=True, channels="BGR")
                else:
                    st.error(f"No '{target_object}' found.")
                    st.warning(
                        "The AI is too 'picky' for this image. Try lowering the Confidence in the sidebar.")
