import cv2
import numpy as np
from ultralytics import YOLO
import cv2
import math 


def find_screen(frame):
    # return (0, 0, 1000, 1000)
    # model
    model = YOLO("yolo-Weights/yolov8n.pt")
    # model = YOLO("best.pt")

    results = model(frame, stream=True)

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
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # class name
        cls = int(best.cls[0])
        # print("Class name -->", classNames[cls])

        # object details
        org = [x1, y1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2

        cv2.putText(frame, r.names[cls], org, font, fontScale, color, thickness)

        return x1, y1, x2, y2

# Function to detect laptop screen outline
def detect_laptop_screen(frame, coords):
    # x1, y1, x2, y2 = coords

    # Convert frame to grayscale
    # gray = cv2.cvtColor(frame[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 350, 400)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the contour with the largest area (assuming it's the laptop screen)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Approximate the contour to a polygon
        epsilon = 0.01 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)

        # for i in range(len(approx)):
        #     approx[i][0][0] += x1
        #     approx[i][0][1] += y1
        
        # Draw the outline of the laptop screen
        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
        
        # Calculate the centroid of the contour
        M = cv2.moments(approx)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroid = (cx, cy)
            cv2.circle(frame, centroid, 5, (255, 0, 0), -1)
            
            # Assume the laptop screen is parallel to the image plane and estimate depth based on size
            # You might need additional calibration for more accurate depth estimation
            depth = 1000  # Arbitrary depth value for demonstration
            # Compute 3D coordinates
            x_3d = (cx - frame.shape[1]/2) * depth / (frame.shape[1]/2)
            y_3d = (cy - frame.shape[0]/2) * depth / (frame.shape[0]/2)
            z_3d = depth
            # Print 3D coordinates
            print("3D Coordinates (x, y, z):", (x_3d, y_3d, z_3d))
        
    return frame


def main():
    cap = cv2.VideoCapture(0)  # Use the default camera
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        
        # coords = find_screen(frame)
        coords = True

        if coords is not None:
            # Detect laptop screen outline
            frame_with_outline = detect_laptop_screen(frame, coords)
            
            # Display the frame
            cv2.imshow('Laptop Screen Detection', frame_with_outline)
        
        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
