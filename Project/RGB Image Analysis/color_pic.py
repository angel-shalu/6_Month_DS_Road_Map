import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Streamlit page setup
st.set_page_config(page_title="My Image", layout="wide")

# Title of the app
st.title("It's Me - Multi-Color Channel Visualizer")

# Load image from local path
@st.cache_data(show_spinner=False)
def load_image():
    path = r"C:\Users\shali\Pictures\Photo.jpg"  # Update to your image path
    return Image.open(path).convert("RGB")

# Load and display the original image
shalini = load_image()
st.image(shalini, caption="My Original Image", use_container_width=True)

# Convert to NumPy array and extract RGB channels
shalini_np = np.array(shalini)
R, G, B = shalini_np[:, :, 0], shalini_np[:, :, 1], shalini_np[:, :, 2]

# Create Red, Green, Blue images
red_img = np.zeros_like(shalini_np)
green_img = np.zeros_like(shalini_np)
blue_img = np.zeros_like(shalini_np)

red_img[:, :, 0] = R
green_img[:, :, 1] = G
blue_img[:, :, 2] = B

# Create Yellow (R + G), Cyan (G + B), Orange (R + 0.5*G)
yellow_img = np.zeros_like(shalini_np)
cyan_img = np.zeros_like(shalini_np)
orange_img = np.zeros_like(shalini_np)

yellow_img[:, :, 0] = R
yellow_img[:, :, 1] = G

cyan_img[:, :, 1] = G
cyan_img[:, :, 2] = B

orange_img[:, :, 0] = R
orange_img[:, :, 1] = (0.5 * G).astype(np.uint8)  # Approximate orange

# Display the 6 color channels
st.subheader("RGB + Composite Channel Visualization")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.image(red_img, caption="Red Channel", use_container_width=True)

with col2:
    st.image(green_img, caption="Green Channel", use_container_width=True)

with col3:
    st.image(blue_img, caption="Blue Channel", use_container_width=True)

with col4:
    st.image(yellow_img, caption="Yellow Channel (Red + Green)", use_container_width=True)

with col5:
    st.image(cyan_img, caption="Cyan Channel (Green + Blue)", use_container_width=True)

with col6:
    st.image(orange_img, caption="Orange Channel (Red + 0.5 Green)", use_container_width=True)

# Grayscale + Colormap section
st.subheader("Colormapped Grayscale Image")

colormap = st.selectbox(
    "Choose a Matplotlib colormap:",
    ["viridis", "plasma", "inferno", "magma", "cividis", "hot", "cool", "gray",'flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                      'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                      'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                      'turbo', 'nipy_spectral', 'gist_ncar']
)

# Convert to grayscale and display with selected colormap
shalini_gray = shalini.convert("L")
shalini_gray_np = np.array(shalini_gray)

fig, ax = plt.subplots(figsize=(6, 4))
ax.imshow(shalini_gray_np, cmap=colormap)
ax.axis("off")  # Hide axes for clean display

# Show plot in Streamlit
st.pyplot(fig)
