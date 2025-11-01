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

# Set up the game window for drawing on top of the camera feed
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw with Your Hand!")

# Colors
WHITE = (255, 255, 255)
BRUSH_COLOR = (0, 255, 0)

# Hand Tracking Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

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
    wrist_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame_width)
    wrist_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame_height)
    return wrist_x, wrist_y

# Main loop
def main():
    # Set up the webcam capture
    cap = cv2.VideoCapture(0)  # Initialize webcam
    clock = pygame.time.Clock()

    # Initialize previous position for drawing
    last_position = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally (mirror effect)
        frame = cv2.flip(frame, 1)

        # Detect hand landmarks
        hand_landmarks = detect_hand_gesture(frame)
        
        # Draw on the screen if hand is detected
        if hand_landmarks:
            wrist_x, wrist_y = hand_to_screen_coordinates(hand_landmarks, WIDTH, HEIGHT)

            # Draw a line from the last position to the new wrist position
            if last_position:
                pygame.draw.line(screen, BRUSH_COLOR, last_position, (wrist_x, wrist_y), BRUSH_SIZE)
            
            last_position = (wrist_x, wrist_y)

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
