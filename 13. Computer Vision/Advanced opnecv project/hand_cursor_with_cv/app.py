import cv2
import mediapipe as mp
import pygame

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 640, 480
FPS = 60
BRUSH_SIZE = 10

# Set up game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw with Your Hand!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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
    screen.fill(WHITE)  # Fill the screen with white background

    cap = cv2.VideoCapture(0)  # Initialize webcam
    clock = pygame.time.Clock()

    last_position = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally (mirror effect)
        frame = cv2.flip(frame, 1)

        # Detect hand landmarks
        hand_landmarks = detect_hand_gesture(frame)
        
        # If hand is detected, draw on the screen
        if hand_landmarks:
            wrist_x, wrist_y = hand_to_screen_coordinates(hand_landmarks, WIDTH, HEIGHT)

            # Draw a circle or brush where the hand's wrist is located
            if last_position:
                pygame.draw.line(screen, BRUSH_COLOR, last_position, (wrist_x, wrist_y), BRUSH_SIZE)
            
            last_position = (wrist_x, wrist_y)

        # Show the webcam feed (for user to see hand movement)
        cv2.imshow("Hand Tracking Feed", frame)

        # Draw the pygame surface
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

        clock.tick(FPS)  # Control the frame rate

if __name__ == "__main__":
    main()
