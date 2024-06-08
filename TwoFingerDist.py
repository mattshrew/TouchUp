import mediapipe as mp
import cv2
from collections import deque
from copy import deepcopy
import math

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Define the maximum number of frames to store in the deques
MAX_FRAMES = 20
# Create deques to store world landmarks data of the tip of the pointer finger and middle finger
pointer_tip_data = deque(maxlen=MAX_FRAMES)
middle_finger_data = deque(maxlen=MAX_FRAMES)

while True:
    success, frame = cap.read()
    if success:
        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(RGB_frame)
        if result.multi_hand_landmarks and len(result.multi_hand_landmarks) < 2:
            hand_landmarks = result.multi_hand_landmarks[0]
            # Extract world coordinates of the tip of the pointer finger (Landmark 8)
            pointer_tip = hand_landmarks.landmark[8]
            pointer_tip_world_coords = (pointer_tip.x, pointer_tip.y, pointer_tip.z)
            # Append the world coordinates to the deque
            pointer_tip_data.append(pointer_tip_world_coords)
            
            # Extract world coordinates of Landmark 12 (middle finger)
            middle_finger = hand_landmarks.landmark[12]
            middle_finger_world_coords = (middle_finger.x, middle_finger.y, middle_finger.z)
            # Append the world coordinates to the deque
            middle_finger_data.append(middle_finger_world_coords)
            
            # Calculate the distance between the most recent points
            if len(pointer_tip_data) > 0 and len(middle_finger_data) > 0:
                pt_coords = pointer_tip_data[-1]
                mf_coords = middle_finger_data[-1]
                distance = math.sqrt((pt_coords[0] - mf_coords[0]) ** 2 +
                                     (pt_coords[1] - mf_coords[1]) ** 2 +
                                     (pt_coords[2] - mf_coords[2]) ** 2)
                print(f"Distance: {distance}")

                # Determine if the fingers are together
                fingers_together = 0 <= distance <= 0.15
                print(f"Fingers Together: {fingers_together}")

            # Create a new landmark list containing only landmarks 8 and 12
            two_landmarks = deepcopy(hand_landmarks)
            for i, landmark in enumerate(two_landmarks.landmark):
                if i != 8 and i != 12:
                    landmark.x = landmark.y = landmark.z = 0

            # Draw only landmarks 8 and 12
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=two_landmarks,
                connections=None,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=5, circle_radius=5),
                connection_drawing_spec=None
            )

        # process to close camera window 
        cv2.imshow("capture image", frame)
        if cv2.waitKey(1) == ord('q'):
            break

print("Pointer Tip Data:", pointer_tip_data)
print("Middle Finger Data:", middle_finger_data)

cv2.destroyAllWindows()
