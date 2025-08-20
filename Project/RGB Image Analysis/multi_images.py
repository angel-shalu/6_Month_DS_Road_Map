import streamlit as st
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

# Streamlit page setup
st.set_page_config(page_title="Elephant Image Processor", layout="wide")

# Title of the app
st.title("Elephant Image - Multi-Color Channel Visualizer")

# Load image from URL and cache it
@st.cache_data(show_spinner=False)
def load_image():
    url = "https://upload.wikimedia.org/wikipedia/commons/3/37/African_Bush_Elephant.jpg"
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGB")

# Load and display the original image
elephant = load_image()
st.image(elephant, caption="Original Elephant Image", use_container_width=True)

# Convert to NumPy array and extract RGB channels
elephant_np = np.array(elephant)
R, G, B = elephant_np[:, :, 0], elephant_np[:, :, 1], elephant_np[:, :, 2]

# Create images for each color channel
red_img = np.zeros_like(elephant_np)
green_img = np.zeros_like(elephant_np)
blue_img = np.zeros_like(elephant_np)

red_img[:, :, 0] = R
green_img[:, :, 1] = G
blue_img[:, :, 2] = B

# Display each RGB channel separately
st.subheader("RGB Channel Visualization")
col1, col2, col3 = st.columns(3)

with col1:
    st.image(red_img, caption="Red Channel", use_container_width=True)

with col2:
    st.image(green_img, caption="Green Channel", use_container_width=True)

with col3:
    st.image(blue_img, caption="Blue Channel", use_container_width=True)

# Convert to grayscale and apply selected colormap
st.subheader("Colormapped Grayscale Image")

colormap = st.selectbox(
    "Choose a Matplotlib colormap:",
    ["viridis", "plasma", "inferno", "magma", "cividis", "hot", "cool", "gray"]
)

# Convert to grayscale and display with selected colormap
elephant_gray = elephant.convert("L")
elephant_gray_np = np.array(elephant_gray)

fig, ax = plt.subplots(figsize=(6, 4))
ax.imshow(elephant_gray_np, cmap=colormap)
ax.axis("off")  # Hide axes for clean display

# Show plot in Streamlit
st.pyplot(fig)
