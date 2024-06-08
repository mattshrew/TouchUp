from ultralytics import YOLO
model = YOLO("yolov8m.pt")

results = model.predict("1.jpg")
result = results[0]

boxes = list(filter(lambda box: result.names[box.cls[0].item()] == 'laptop', result.boxes))

for box in boxes:
    coords = list(map(round, box.xyxy[0].tolist()))
    class_id = result.names[box.cls[0].item()]
    conf = round(box.conf[0].item(), 2)

    print("Object type:", class_id)
    print("Coordinates:", coords)
    print("Probability:", conf)
    print("---")
