from ultralytics import YOLO
import cv2
import math 
# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# model
model = YOLO("yolo-Weights/yolov8n.pt")
# model = YOLO("best.pt")

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # coordinates
    best = None
    best_confidence = -1e9
    for r in results:
        boxes = list(filter(lambda box: r.names[box.cls[0].item()] in {'tablet', 'desktop', 'laptop'}, r.boxes))

        for box in boxes:
            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            # print("Confidence --->",confidence)
            if confidence > best_confidence:
                best_confidence = confidence
                best = box

    # bounding box
    if best is not None:
        x1, y1, x2, y2 = map(int, best.xyxy[0])

        # put box in cam
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # class name
        cls = int(best.cls[0])
        # print("Class name -->", classNames[cls])

        # object details
        org = [x1, y1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2

        cv2.putText(img, r.names[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()