import cv2
import numpy as np

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Assume the screen is the largest quadrilateral
    screen_cnt = None
    max_area = 0
    for cnt in contours:
        epsilon = 0.1 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if len(approx) == 4:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                screen_cnt = approx

    # Draw the screen contour
    cv2.drawContours(frame, [screen_cnt], -1, (0, 255, 0), 3)
    print(screen_cnt)

    cv2.imshow("Object Detection", frame)
