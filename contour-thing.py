import cv2
import numpy as np
from time import perf_counter as pf

video = cv2.VideoCapture(0)

start = pf()
largests = [None] * 3
largest_areas = [-1e9] * 3
while True and pf() - start < 10:
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

    if max_area > largest_areas[-1]:
       largest_areas.pop()
       largests.pop()
       largest_areas.append(max_area)
       largest_areas.sort(reverse=True)
       largests.insert(largest_areas.index(max_area), screen_cnt)

    # Draw the screen contour
    cv2.drawContours(frame, [screen_cnt], -1, (0, 255, 0), 3)
    # print(screen_cnt)

    cv2.imshow("Object Detection", frame)

print([list(largests[-1][i][0]) for i in range(len(largests[-1]))])

while True:
    ret, frame = video.read()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    cv2.drawContours(frame, [largests[-1]], -1, (255, 0, 0), 3)

    for i in range(len(largests[-1])):
        # print(largest[i][0])
        cv2.circle(frame, largests[-1][i][0], 3, (0,0,255), cv2.FILLED)

    cv2.imshow("Object Detection", frame)

"""[[353, 270], [344, 407], [580, 450], [585, 282]]"""