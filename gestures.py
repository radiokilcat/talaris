import cv2
import mediapipe as mp
from pynput.mouse import Controller, Button
from screeninfo import get_monitors
import math
import argparse
import time
from Cursor import Cursor
from Scroll import Scroll
import easingFunctions
import handConditions

parser = argparse.ArgumentParser(description="Hand Tracking")
parser.add_argument("--no-video", action="store_true", help="Run without displaying the video window")
args = parser.parse_args()

monitor = get_monitors()[0]
screen_width, screen_height = monitor.width, monitor.height

cap = cv2.VideoCapture(0)
mouse = Controller()

hands = mp.solutions.hands.Hands(static_image_mode=False,
                                 max_num_hands=2,
                                 min_tracking_confidence=0.9,
                                 min_detection_confidence=0.9)

mpDraw = mp.solutions.drawing_utils
cursor = Cursor()
scroll = Scroll()

prev_time = time.time()
smoothing_factor = 0.1
velocity_scaling = 0.2
scroll_scaling = 0.1
prev_positions = {"Right": (None, None), "Left": (None, None)}
velocities = {"Right": (0, 0), "Left": (0, 0)}
inertia_threshold = 10

while True:
    success, img = cap.read()
    if not success:
        break
    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time
    
    result = hands.process(img)
    if result.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            if not args.no_video:
                mpDraw.draw_landmarks(img, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            hand_label = handedness.classification[0].label
            index_finger_tip = hand_landmarks.landmark[8]
            h, w, _ = img.shape
            # Convert normalized index finger tip position to image coordinates
            img_x = int(index_finger_tip.x * w)
            img_y = int(index_finger_tip.y * h)

            # Map image coordinates to screen coordinates
            screen_x = int(img_x * screen_width / w)
            screen_y = int(img_y * screen_height / h)

            # mirror x
            screen_x = screen_width - screen_x
            
            # current_pos = (int(screen_x * screen_width / w), int(index_finger_tip.y * screen_height / h ))
            current_pos = (int(screen_x), int(screen_y))
            print(f"current pos: {current_pos} index_finger_tip.x: {index_finger_tip.x}, index_finger_tip.y: {index_finger_tip.y}")
            print(f"screen_width: {screen_width} screen_height: {screen_height}, w: {w}, h: {h}")

            if hand_label == "Left":
                cursor.update_position(current_pos)

            elif hand_label == "Right":
                if handConditions.are_fingers_close(hand_landmarks.landmark):
                    print("fingers are close")
                    # smoothed_scroll = velocities["Right"][1] * scroll_scaling * velocity_scaling
                    scroll.update_scroll(10)

    if not args.no_video:
        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if not args.no_video:
    cap.release()
    cv2.destroyAllWindows()