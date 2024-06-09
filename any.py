import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import pyautogui
import time
import math

# Number of frames to consider for stability
STABILITY_FRAMES = 5
CURSOR_DELAY = 0.1  # Adjust this value as needed

def heightf(length):
    distance = (2546 + -4.32*(length) + 2.35*10**(-3)*(length**2))-608
    # print(distance)
    return distance

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def main():
    cap = cv2.VideoCapture(0)

    line_found = False  # Flag to indicate if the blue horizontal line has been found
    line_positions = []
    stable_avg_top_row_y = None  # Variable to store the stable position of the top row
    above_line_deque = deque(maxlen=20)
    click = False
    x_positions = []  # List to record x-positions of crossing points

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    x_origin = None  # Variable to store the x-origin
    keyboard_width = None  # Variable to store the width of the keyboard

    start_time = time.time()
    last_move_time = time.time()
    click_time = None

    while line_found is False or time.time() - start_time < 10:
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find the best possible blue horizontal line only once
        if not line_found:
            # Your code to find the blue horizontal line goes here
            # Once found, set line_found to True
             # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply GaussianBlur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Perform edge detection using Canny
            edges = cv2.Canny(blurred, 50, 150)

            # Find contours
            contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filter out small contours
            min_contour_area = 1000  # Adjust this threshold as needed
            large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

            # Filter out non-rectangular contours
            rectangular_contours = []
            for contour in large_contours:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h
                if 0.5 < aspect_ratio < 2:  # Adjust this range as needed
                 rectangular_contours.append(contour)

            # Check if there are any rectangular contours
            if rectangular_contours:
                # Find the top edge of the top row of keys
                top_row_y = min([cv2.boundingRect(contour)[1] for contour in rectangular_contours])

                # Find the leftmost edge of the keyboard (x-origin) and the width of the keyboard
                if x_origin is None:
                    x_origin = min([cv2.boundingRect(contour)[0] for contour in rectangular_contours])
                    keyboard_width = max([cv2.boundingRect(contour)[0] + cv2.boundingRect(contour)[2] for contour in rectangular_contours]) - x_origin

                # Store the current position of the line
                line_positions.append(top_row_y)

                # Keep only the last STABILITY_FRAMES positions
                line_positions = line_positions[-STABILITY_FRAMES:]


                # Calculate the average position of the line
                if len(line_positions) > 0:
                    avg_top_row_y = int(sum(line_positions) / len(line_positions))
                else:
                    avg_top_row_y = 0

                # Update the stable position of the line if necessary
                if stable_avg_top_row_y is None:
                    stable_avg_top_row_y = avg_top_row_y

                # Use the stable average position of the line if available
                if stable_avg_top_row_y is not None:
                    avg_top_row_y = stable_avg_top_row_y
                else:
                    avg_top_row_y = 0

                # Draw a continuous horizontal line at the average position of the line
                cv2.line(frame, (0, stable_avg_top_row_y), (frame.shape[1], stable_avg_top_row_y), (255, 0, 0), 2)

                # Draw contours on the frame
                cv2.drawContours(frame, rectangular_contours, -1, (0, 255, 0), 2)

                # Display the frame
                cv2.imshow('Keyboard Contour Detection', frame)

                line_found = True

    print("done")

    while True:
        ret, frame = cap.read()
        if not ret: continue

        # Detect hand landmarks
        results = hands.process(rgb_frame)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Check if hand landmarks are detected
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]  # Assuming only one hand is detected
            index_finger_tip = hand_landmarks.landmark[8]  # Landmark 8 is the tip of the index finger

            # Get index finger tip coordinates in pixel values
            height, width, _ = frame.shape
            index_finger_x = int(index_finger_tip.x * width)
            index_finger_y = int(index_finger_tip.y * height)

            # Adjust the x-coordinate based on the x-origin
            if x_origin is not None:
                adjusted_index_finger_x = index_finger_x - x_origin
            else:
                adjusted_index_finger_x = index_finger_x

            # Scale the x-position relative to the width of the keyboard to match the width of the screen
            if keyboard_width is not None:
                scaled_index_finger_x = int((adjusted_index_finger_x / keyboard_width) * width)
            else:
                scaled_index_finger_x = index_finger_x

            landmarks = hand_landmarks.landmark
            x6, y6 = landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].x, landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
            x8, y8 = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

            # Calculate distance between landmarks 6 and 8
            length_between_landmarks = calculate_distance(x6 * frame.shape[1], y6 * frame.shape[0], x8 * frame.shape[1], y8 * frame.shape[0])

            # Move the cursor vertically based on the finger position
            scaled_index_finger_y = heightf(length_between_landmarks)

            # Draw a circle at the index finger tip
            cv2.circle(frame, (index_finger_x, index_finger_y), 5, (0, 0, 255), -1)

            # Check if index finger tip is above the blue horizontal line
            above_line = index_finger_y < avg_top_row_y
            above_line_deque.append(above_line)

            # Check for crossing event and record x-position if crossing from below to above
            if len(above_line_deque) >= 2 and above_line_deque[-2] == False and above_line_deque[-1] == True:
                x_positions.append(scaled_index_finger_x)

            # Move the cursor horizontally with a delay to synchronize with finger movement
            current_time = time.time()
            if current_time - last_move_time > CURSOR_DELAY:
                pyautogui.moveTo(scaled_index_finger_x, scaled_index_finger_y)
                last_move_time = current_time

            # Check if there are 5 consecutive "True" or "False" values in the deque
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

            # Perform click if the finger remains above the line for a certain duration
            if click and time.time() - click_time > 0.5:  # Adjust the duration as needed
                if x_positions:
                    pyautogui.click(x=x_positions[-1], y=scaled_index_finger_y, duration=0.1)  # Perform click at the last recorded x-position
            elif not click and click_time:
                click_time = None

        # Draw a continuous horizontal line at the average position of the line
        cv2.line(frame, (0, stable_avg_top_row_y), (frame.shape[1], stable_avg_top_row_y), (255, 0, 0), 2)
        # Display the frame
        cv2.imshow('Keyboard Contour Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
