import cv2
import mediapipe as mp
from screeninfo import get_monitors
from pynput.mouse import Controller
from gestures import *

cap = cv2.VideoCapture(0)
mouse = Controller()

monitor = get_monitors()[1]
screen_width, screen_height = monitor.width, monitor.height

hands = mp.solutions.hands.Hands(static_image_mode=False,
                                 max_num_hands=1,
                                 min_tracking_confidence=0.5,
                                 min_detection_confidence=0.5)

mpDraw = mp.solutions.drawing_utils
prev_cx, prev_cy = 0, 0
smoothing_factor = 0.8

while True:
    _, img = cap.read()
    result = hands.process(img)
    if result.multi_hand_landmarks:
        for id, lm in enumerate(result.multi_hand_landmarks[0].landmark):
            h, w, _ = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 3, (255, 0, 255))
            if id == 8:
                cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                smoothed_cx = prev_cx + (cx - prev_cx) * (1 - smoothing_factor)
                smoothed_cy = prev_cy + (cy - prev_cy) * (1 - smoothing_factor)
                mouse.position = (smoothed_cx * screen_width / w, smoothed_cy * screen_height / h)
                
    cv2.imshow("hand tracking", img)
    cv2.waitKey(1)