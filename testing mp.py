import mediapipe as mp
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

while True:
    success, frame = cap.read()
    if success:
        RGB_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = hand.process(RGB_frame)
        if result.multi_hand_landmarks:
            print(len(result.multi_hand_landmarks[0].landmark))
            for hand_landmarks in result.multi_hand_landmarks:
                # mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                pass
        cv2.imshow("capture image", frame)
        if cv2.waitKey(1)==ord('q'):
            break

cv2.destroyAllWindows()