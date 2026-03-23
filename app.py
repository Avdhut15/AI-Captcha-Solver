"""The professional Streamlit interface with Visual Overlay support."""
import streamlit as st
from PIL import Image
from engine.captcha_engine import create_engine

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
            # Create engine and solve
            engine = create_engine()
            result = engine.solve(
                img,
                target_object=target_object,
                conf=conf_val,
                manual_grid=manual_grid if manual_grid > 0 else None
            )

            with col2:
                if result['success']:
                    st.success(
                        f"Grid: {result['grid_size']}x{result['grid_size']}")
                    st.markdown(
                        f"### 👉 **Click Squares: {result['solution']}**")
                    st.image(
                        result['visual'], caption="AI Solution (Grid + Highlights)", use_container_width=True)
                else:
                    st.error(f"AI could not find any '{target_object}'.")
                    st.info("Try lowering the Confidence slider in the sidebar.")
