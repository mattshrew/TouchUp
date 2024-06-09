import cv2
import numpy as np
import mediapipe as mp
from collections import deque
from pynput.mouse import Controller, Button
import time
import math

STABILITY_FRAMES = 5
CURSOR_DELAY = 0.1

def heightf(length):
    return (2546 + -4.32 * length + 2.35 * 10 ** (-3) * (length ** 2)) - 608

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def any_touch():
    cap = cv2.VideoCapture(0)
    hands = mp.solutions.hands.Hands(
        static_image_mode=False, max_num_hands=1,
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    )
    mouse = Controller()

    line_found = False
    line_positions = deque(maxlen=STABILITY_FRAMES)
    stable_avg_top_row_y = None
    above_line_deque = deque(maxlen=20)
    click = False
    x_positions = []

    x_origin, keyboard_width = None, None
    start_time = time.time()
    last_move_time, click_time = time.time(), None

    while not line_found or time.time() - start_time < 10:
        ret, frame = cap.read()
        if not ret:
            continue

        if not line_found:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)
            contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]
            rectangular_contours = [cnt for cnt in large_contours if 0.5 < cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3] < 2]

            if rectangular_contours:
                top_row_y = min(cv2.boundingRect(cnt)[1] for cnt in rectangular_contours)
                if x_origin is None:
                    x_origin = min(cv2.boundingRect(cnt)[0] for cnt in rectangular_contours)
                    keyboard_width = max(cv2.boundingRect(cnt)[0] + cv2.boundingRect(cnt)[2] for cnt in rectangular_contours) - x_origin

                line_positions.append(top_row_y)
                avg_top_row_y = int(sum(line_positions) / len(line_positions))
                stable_avg_top_row_y = stable_avg_top_row_y or avg_top_row_y

                cv2.line(frame, (0, stable_avg_top_row_y), (frame.shape[1], stable_avg_top_row_y), (255, 0, 0), 2)
                cv2.drawContours(frame, rectangular_contours, -1, (0, 255, 0), 2)
                cv2.imshow('Keyboard Contour Detection', frame)

                line_found = True

    print("done")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            index_finger_tip = hand_landmarks.landmark[8]

            height, width, _ = frame.shape
            index_finger_x = int(index_finger_tip.x * width)
            index_finger_y = int(index_finger_tip.y * height)

            adjusted_index_finger_x = index_finger_x - (x_origin or 0)
            scaled_index_finger_x = int((adjusted_index_finger_x / (keyboard_width or width)) * width)

            landmarks = hand_landmarks.landmark
            x6, y6 = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP].x, landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP].y
            x8, y8 = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].x, landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y
            length_between_landmarks = calculate_distance(x6 * width, y6 * height, x8 * width, y8 * height)

            scaled_index_finger_y = heightf(length_between_landmarks)

            cv2.circle(frame, (index_finger_x, index_finger_y), 5, (0, 0, 255), -1)

            above_line = index_finger_y < stable_avg_top_row_y
            above_line_deque.append(above_line)

            if len(above_line_deque) >= 2 and not above_line_deque[-2] and above_line_deque[-1]:
                x_positions.append(scaled_index_finger_x)

            current_time = time.time()
            if current_time - last_move_time > CURSOR_DELAY:
                mouse.position = (scaled_index_finger_x, scaled_index_finger_y)
                last_move_time = current_time

            if len(above_line_deque) >= 5:
                if all(above_line_deque[i] for i in range(-5, 0)):
                    if not click:
                        click = True
                        cv2.circle(frame, (index_finger_x, index_finger_y), 5, (0, 255, 0), -1)
                        click_time = time.time()
                elif all(not above_line_deque[i] for i in range(-5, 0)):
                    if click:
                        click = False
                        click_time = None

            if click and time.time() - click_time > 0.5:
                if x_positions:
                    mouse.click(Button.left, 1)
            elif not click and click_time:
                click_time = None

        cv2.line(frame, (0, stable_avg_top_row_y), (frame.shape[1], stable_avg_top_row_y), (255, 0, 0), 2)
        cv2.imshow('Keyboard Contour Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    any_touch()
