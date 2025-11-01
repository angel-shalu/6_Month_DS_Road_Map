import cv2
import mediapipe as mp
import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 640, 480
FPS = 60
BRUSH_SIZE = 10
MASK_COLOR = (0, 0, 0)  # Color for the mask (black)

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw on Face with Finger!")

# Colors
WHITE = (255, 255, 255)
BRUSH_COLOR = (0, 255, 0)

# Hand Tracking Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Face Detection Setup (Using Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to detect hand gestures and draw
def detect_hand_gesture(frame):
    # Convert the frame to RGB for hand tracking
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    hand_landmarks = None
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            hand_landmarks = hand

    return hand_landmarks

# Function to convert hand coordinates to screen coordinates
def hand_to_screen_coordinates(hand_landmarks, frame_width, frame_height):
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    x = int(index_finger_tip.x * frame_width)
    y = int(index_finger_tip.y * frame_height)
    return x, y

# Function to detect faces and return the face region
def detect_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)  # Detect faces

    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]  # Region of interest for the face
        return (x, y, w, h), face_roi
    return None, None

# Main loop
def main():
    # Set up the webcam capture
    cap = cv2.VideoCapture(0)  # Initialize webcam
    clock = pygame.time.Clock()

    # Initialize previous position for drawing
    last_position = None
    mask_image = None  # Store the mask image

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally (mirror effect)
        frame = cv2.flip(frame, 1)

        # Detect face and apply a mask to the face region
        face_coords, face_roi = detect_face(frame)
        if face_coords:
            x, y, w, h = face_coords
            # Create a blank mask over the face region
            if mask_image is None:
                mask_image = np.zeros_like(frame)
            mask_image[y:y+h, x:x+w] = (0, 0, 0)  # Black mask on face

        # Detect hand landmarks
        hand_landmarks = detect_hand_gesture(frame)
        
        # Draw on the screen if hand is detected
        if hand_landmarks:
            x, y = hand_to_screen_coordinates(hand_landmarks, WIDTH, HEIGHT)

            # Draw a circle at the finger tip position (for drawing)
            if last_position:
                # Draw line from last finger position to current position
                pygame.draw.line(screen, BRUSH_COLOR, last_position, (x, y), BRUSH_SIZE)
            
            # Update last position
            last_position = (x, y)

        # If there's a mask (from finger drawing), apply it over the face region
        if mask_image is not None:
            frame = cv2.addWeighted(frame, 1, mask_image, 0.5, 0)  # Merge mask with webcam frame

        # Convert the OpenCV frame to a format suitable for pygame (Surface)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame_rgb)

        # Display the webcam feed as the background
        screen.blit(frame_surface, (0, 0))

        # Update the screen with the drawing on top of the camera feed
        pygame.display.update()

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                cv2.destroyAllWindows()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                cap.release()
                pygame.quit()
                cv2.destroyAllWindows()
                return

        # Frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()
