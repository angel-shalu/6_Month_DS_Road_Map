
import numpy as np
import cv2

# Load the face and eye Haar cascade classifiers
face_classifier = cv2.CascadeClassifier(r"C:\Users\shali\Desktop\DS_Road_Map\13. Computer Vission\opencv master data-haarcascades\Haarcascades\haarcascade_frontalface_default.xml")
eye_classifier = cv2.CascadeClassifier(r"C:\Users\shali\Desktop\DS_Road_Map\13. Computer Vission\opencv master data-haarcascades\Haarcascades\haarcascade_eye.xml")

# Load the image
#img = cv2.imread(r"C:\Users\A3MAX SOFTWARE TECH\Desktop\WORK\1. KODI WORK\1. NARESH\10. WORKSHOP\7. Exploring Generative AI through computer vision\myimage.jpg")
#img = cv2.imread(r"C:\Users\A3MAX SOFTWARE TECH\Desktop\WORK\2. DATASCIENCE PROJECT\10. Computer vision\computer vison\opencv\image_examples\5.jpg")#img = cv2.imread(r"C:\Users\Admin\Desktop\NIT\1. NIT_Batches\10. WORKSHOP\2024 - WORKSHOP\7. Exploring Generative AI through computer vision\myimage.jpg")
img = cv2.imread(r"C:\Users\shali\Pictures\WhatsApp Image 2025-06-16 at 21.55.01_e3812112.jpg")
#img = cv2.imread(r"C:\Users\Admin\Desktop\NIT\1. NIT_Batches\10. WORKSHOP\2024 - WORKSHOP\7. Exploring Generative AI through computer vision\myimage.jpg")

# Check if the image is loaded correctly
if img is None:
    print("Error: Image not found or cannot be loaded!")
    exit()  # Exit if image is not loaded

# Convert image to grayscale for face detection
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_classifier.detectMultiScale(gray, 1.3, 5)

# Check if faces are detected
if len(faces) == 0:
    print("No Face Found")

# Draw rectangles around detected faces and detect eyes within each face
for (x, y, w, h) in faces:
    # Draw a rectangle around the face
    cv2.rectangle(img, (x, y), (x + w, y + h), (127, 0, 255), 2)
    
    # Region of interest (ROI) for face
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = img[y:y + h, x:x + w]

    # Detect eyes within the face region
    eyes = eye_classifier.detectMultiScale(roi_gray)

    for (ex, ey, ew, eh) in eyes:
        # Draw rectangle around each detected eye
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 255, 0), 2)

# Display the output image with rectangles around faces and eyes
cv2.imshow('img', img)

# Wait for a key press before closing the window
cv2.waitKey(0)

# Destroy all OpenCV windows
cv2.destroyAllWindows()
