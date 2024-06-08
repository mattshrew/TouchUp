import mediapipe as mp
import cv2
from collections import deque

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Define the maximum number of frames to store in the deque
MAX_FRAMES = 20
# Create a deque to store world landmarks data of the tip of the pointer finger
pointer_tip_data = deque(maxlen=MAX_FRAMES)

while True:
    success, frame = cap.read()
    if success:
        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(RGB_frame)
        if result.multi_hand_landmarks and len(result.multi_hand_landmarks) < 2:
            hand_landmarks = result.multi_hand_landmarks[0]
            # Extract world coordinates of the tip of the pointer finger
            pointer_tip = hand_landmarks.landmark[8]
            pointer_tip_world_coords = (pointer_tip.x, pointer_tip.y, pointer_tip.z)
            # Append the world coordinates to the deque
            pointer_tip_data.append(pointer_tip_world_coords)
            
            # Create a new landmark list containing only landmark 8
            from copy import deepcopy
            single_landmark = deepcopy(hand_landmarks)
            for i, landmark in enumerate(single_landmark.landmark):
                if i != 8:
                    landmark.x = landmark.y = landmark.z = 0

            # Draw only landmark 8
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=single_landmark,
                connections=None,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=5, circle_radius=5),
                connection_drawing_spec=None
            )

        # process to close camera window 
        cv2.imshow("capture image", frame)
        if cv2.waitKey(1) == ord('q'):
            break

print(pointer_tip_data)
print(pointer_tip_data[-1])

cv2.destroyAllWindows()
