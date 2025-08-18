import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

# Function to load image from URL
def load_image_from_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# Load elephant image
elephant_url = "https://upload.wikimedia.org/wikipedia/commons/3/37/African_Bush_Elephant.jpg"
elephant = load_image_from_url(elephant_url)

# Display the original elephant image
plt.figure(figsize=(6, 4))
plt.imshow(elephant)
plt.title("Elephant - Original")
plt.axis("off")
plt.show()

# Convert image to NumPy array
elephant_np = np.array(elephant)
print("Elephant Image Shape:", elephant_np.shape)

# Convert to grayscale
elephant_gray = elephant.convert("L")
elephant_gray_np = np.array(elephant_gray)

# Display grayscale image
plt.figure(figsize=(6, 4))
plt.imshow(elephant_gray_np, cmap="gray")  # Use a valid grayscale colormap
plt.title("Elephant - Grayscale")
plt.axis("off")
plt.show()
