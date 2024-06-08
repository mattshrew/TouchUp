import cv2
import mediapipe as mp
import time
from pynput.mouse import Button, Controller
import pyautogui as gui

cap = cv2.VideoCapture(2)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands = 2, min_detection_confidence = 0.75, model_complexity=1)
mpDraw = mp.solutions.drawing_utils

# Mouse Setup
mouse = Controller()
currentPos = mouse.position
mouseDown = False
rightDown = False

# Dimensions setup
sWidth, sHeight = gui.size()
lastXPos = sWidth / 2
lastYPos = sHeight / 2

# First iteration
first = True

# Arrays to store calculations for last 6 frames for the purpose of creating moving averages to smooth out mouse motion
# (Sacrifices a bit of latency for smoothness)
xDiffs = []
for i in range(8):
	xDiffs.append(0)

yDiffs = []
for i in range(8):
	yDiffs.append(0)

leftStart = time.time()
rightStart = time.time()

while True:

	# Prevents the mouse from getting stuck in the edges of the screen
	mouseX, mouseY = mouse.position
	if mouseX > sWidth:
		mouse.position = (sWidth, mouseY)
		mouseX = sWidth
	if mouseX < 0:
		mouse.position = (0, mouseY)
		mouseX = 0
	if mouseY > sHeight:
		mouse.position = (mouseX, sHeight)
		mouseY = sHeight
	if mouseY < 0:
		mouse.position = (mouseX, 0)
		mouseY = 0
	success, frame = cap.read()
	frame = cv2.flip(frame, 1)

	imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	results = hands.process(imgRGB)


	if results.multi_hand_landmarks:
		# mpDraw.draw_landmarks(frame, results.multi_hand_landmarks[0])

		# First hand landmarks (fing stands for finger)
		pointHand = results.multi_hand_landmarks[0]
		fing1 = pointHand.landmark[8]
		fing2 = pointHand.landmark[4]
		fing3 = pointHand.landmark[12]
		pointer = pointHand.landmark[0]


		if len(results.multi_hand_landmarks) >= 2:
			# Redefines some variables so the hands don't switch when a second hand comes into frame
			pointHand = results.multi_hand_landmarks[1]
			fing1 = pointHand.landmark[8]
			fing2 = pointHand.landmark[4]
			fing3 = pointHand.landmark[12]
			pointer = pointHand.landmark[0]

			scroller = results.multi_hand_landmarks[0]
			scrollFing1 = scroller.landmark[8]
			scrollFing2 = scroller.landmark[4]
			scrollFing3 = scroller.landmark[12]

			# Thumb and pointer
			scrollxdif1 = abs(scrollFing1.x - scrollFing2.x)
			scrollydif1 = abs(scrollFing1.y - scrollFing2.y)

			# Thumb and middle finger
			scrollxdif2 = abs(scrollFing2.x - scrollFing3.x)
			scrollydif2 = abs(scrollFing2.y - scrollFing3.y)

			# print("2 hands!")

			if scrollxdif1 < 0.03 and scrollydif1 < 0.03:
				mouse.scroll(0, -3)

			if scrollxdif2 < 0.03 and scrollydif2 < 0.03:
				mouse.scroll(0, 3)


		# Click Script

		# Thumb and pointer
		xdif = abs(fing1.x - fing2.x)
		ydif = abs(fing1.y - fing2.y)

		# Thumb and middle finger
		xdif2 = abs(fing2.x - fing3.x)
		ydif2 = abs(fing2.y - fing3.y)

		# Left Click
		if xdif < 0.03 and ydif < 0.03:
			if not mouseDown:
				if time.time() - leftStart < 0.5:
					mouse.press(Button.left)
					mouseDown = True
				else:
					mouse.click(Button.left)
					leftStart = time.time()
					mouseDown = True
		else:
			if mouseDown:
				mouse.release(Button.left)
				mouseDown = False

		# Right Click
		if xdif2 < 0.03 and ydif2 < 0.03:
			if not rightDown:
				if time.time() - rightStart > 0.75:
					rightDown = True
					mouse.click(Button.right)
					rightStart = time.time()
		else:
			rightDown = False

		# Takes care of the first hand detection, so the mouse doesn't snap to the side of the screen
		if first:
			lastXPos = pointer.x
			lastYPos = pointer.y
			first = False
		
		xDiff = (pointer.x - lastXPos) * 5000
		yDiff = (pointer.y - lastYPos) * 5000

		xDiffs.append(xDiff)
		del xDiffs[0]

		yDiffs.append(yDiff)
		del yDiffs[0]

		xAve = sum(xDiffs)/len(xDiffs)
		yAve = sum(yDiffs)/len(yDiffs)

		# Removes average when mouse is moving fast (disabled for now as it causes more jitter)

		# if xDiff - 20 > xAve and yDiff - 40 < yAve:
		# 	mouse.move(xDiff, yAve)
		# 	print("accelerate1")
		# elif xDiff - 20 < xAve and yDiff - 40 > yAve:
		# 	mouse.move(xAve, yDiff)
		# 	print("accelerate2")
		# elif xDiff - 20 > xAve and yDiff - 40 > yAve:
		# 	mouse.move(xDiff, yDiff)
		# 	print("accelerate3")
		# else:

		# Move the mouse
		mouse.move(xAve, yAve)

		lastXPos = pointer.x
		lastYPos = pointer.y

	else:
		pass
		# print("no hands in frame")
    
    
	# if cv2.waitKey(1) & 0xFF == ord("q"):
	# 	break

	# cv2.imshow("Object Detection", frame)
