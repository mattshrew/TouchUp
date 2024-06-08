'''
Width: 640

Height: 480

0 y = top

0 x = left side
'''

import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
print(cap)
print(cap.isOpened())

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands = 2, min_detection_confidence = 0.75)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


quitFlag = False
quitColor = (0,0,225)
tryQuit = False

leftHand = False
rightHand = False

RightHandOnScreen = False
LeftHandOnScreen = False

rightHandLms = []
leftHandLms = []

mainHand = None

leftBoxColor = (244,244,88)
rightBoxColor = (244,244,88)

tryLeft = False
tryRight = False

trySwitch = False

rightPointerColor = (244,244,88)

while quitFlag == False:
	success, img = cap.read()
	img = cv2.flip(img, 1)
	
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	results = hands.process(imgRGB)

	if results.multi_hand_landmarks:
		RightHandOnScreen = False
		LeftHandOnScreen = False
		for handLms in results.multi_hand_landmarks:
			for id, lm in enumerate(handLms.landmark):
				print(id, lm)
				h, w, c, = img.shape
				cx, cy = int(lm.x*w), int(lm.y*h)

				if id == 0:
					lms_base = lm
				if id == 1:
					lms_side = cx

					if lms_side > (lms_base.x*w):
						leftHand = True
						rightHand = False
					elif lms_side < (lms_base.x*w):
						rightHand = True
						leftHand = False

				if rightHand == True and leftHand == False:
					if id == 1:
						RightHandOnScreen = True
						rightHandLms = []
						rightHandLms.append(lms_base)
						rightHandLms.append(lm)
					else:
						rightHandLms.append(lm)
				elif leftHand == True and rightHand == False:
					if id == 1:
						LeftHandOnScreen = True
						leftHandLms = []
						leftHandLms.append(lms_base)
						leftHandLms.append(lm)
					else:
						leftHandLms.append(lm)

			mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
	else:
		RightHandOnScreen = False
		LeftHandOnScreen = False

	if mainHand == None:
		cv2.putText(img, 'Select Main Hand', (180,250), cv2.FONT_HERSHEY_PLAIN, 2, (244,244,88), 2)
		cv2.rectangle(img, pt1=(100,215), pt2=(150,265), color=leftBoxColor, thickness=4)
		cv2.putText(img, 'L', (110, 255), cv2.FONT_HERSHEY_PLAIN, 3, leftBoxColor, 3)
		cv2.rectangle(img, pt1=(500,215), pt2=(550,265), color=rightBoxColor, thickness=4)
		cv2.putText(img, 'R', (510,255), cv2.FONT_HERSHEY_PLAIN, 3, rightBoxColor, 3)


		if LeftHandOnScreen == True:
			leftHandPointer_x = int((leftHandLms[8].x*w))
			leftHandPointer_y = int((leftHandLms[8].y*h))
			cv2.circle(img, (leftHandPointer_x,leftHandPointer_y), 10, (225,0,0), cv2.FILLED)
			if leftHandPointer_x > 100 and leftHandPointer_x < 150 and leftHandPointer_y > 215 and leftHandPointer_y < 265:
				if tryLeft == False:
					tryLeft = True
					tryRight = False
					leftHandStartT = time.time()
				elif tryLeft == True:
					LeftHandCT = time.time()
					LeftHandT = int((LeftHandCT - leftHandStartT) % 60)
					if LeftHandT == 1:
						leftBoxColor = (255,0,0)
					elif LeftHandT == 2:
						mainHand = 'Left'
			else:
				leftBoxColor = (244,244,88)
				tryLeft = False

		if RightHandOnScreen == True:
			rightHandPointer_x = int((rightHandLms[8].x*w))
			rightHandPointer_y = int((rightHandLms[8].y*h))
			cv2.circle(img, (rightHandPointer_x,rightHandPointer_y), 10, (225,0,0), cv2.FILLED)
			if rightHandPointer_x > 500 and rightHandPointer_x < 550 and rightHandPointer_y > 215 and rightHandPointer_y < 265:
				if tryRight == False:
					tryRight = True
					tryLeft = False
					rightHandStartT = time.time()
				elif tryRight == True:
					RightHandCT =  time.time()
					RightHandT = int((RightHandCT - rightHandStartT) % 60)
					if RightHandT == 1:
						rightBoxColor = (255,0,0)
					elif RightHandT == 2:
						mainHand = 'Right'
			else:
				rightBoxColor = (244,244,88)
				tryRight = False



	if RightHandOnScreen == True:
		if mainHand == 'Right':
			right_pointer_tip_x = int(rightHandLms[8].x*w)
			right_pointer_tip_y = int((rightHandLms[8].y*h))

			if right_pointer_tip_y > int((rightHandLms[6].y*h)):# Pointer Finger
				rightPointerDown = True
			else:
				rightPointerDown = False

			if int((rightHandLms[12].y*h)) > int((rightHandLms[10].y*h)):# Middle Finger
				rightMiddleDown = True
			else:
				rightMiddleDown = False

			if int((rightHandLms[16].y*h)) > int((rightHandLms[14].y*h)):#Ring Finger
				rightRingDown = True
			else:
				rightRingDown = False

			if int((rightHandLms[20].y*h)) > int((rightHandLms[18].y*h)):# Pinkie Finger
				rightPinkieDown = True
			else:
				rightPinkieDown = False

			if int((rightHandLms[4].x*w)) > int((rightHandLms[3].x*w)):# Thumb
				rightThumbDown = True
			else:
				rightThumbDown = False


			if rightPointerDown == True and rightMiddleDown == True and rightRingDown == True and rightPinkieDown == True and rightThumbDown == True:
				rightFist = True
			else:
				rightFist = False

			if rightPointerDown == True and rightMiddleDown == True and rightRingDown == True and rightPinkieDown == False and rightThumbDown == False:
				if trySwitch == False:
					switchStart = time.time()
					trySwitch = True
				elif trySwitch == True:
					switchCT = time.time()
					switchT = int((switchCT - switchStart) % 60)
					if switchT == 1:
						rightPointerColor = (255,0,0)
					elif switchT == 2:
						mainHand = None
			else:
				rightPointerColor = (244,244,88)
				trySwitch = False



			if rightFist != True:
				cv2.circle(img, (right_pointer_tip_x,right_pointer_tip_y), 10, rightPointerColor, cv2.FILLED)
				if right_pointer_tip_x > 540 and right_pointer_tip_x < 620 and right_pointer_tip_y > 20 and right_pointer_tip_y < 60:
					if tryQuit == False:
						print("Trying To Quit")
						tryQuit = True
						StartT = time.time()
					elif tryQuit == True:
						ct = time.time()
						t = int((ct - StartT) % 60)
						#print(t)
						if t == 1:
							quitColor = (0,225,0)
							#print("COLOR BLUE")
						elif t == 2:
							quitColor = (225,0,0)
							#print("COLOR GREEN")
						elif t == 3:
							#print("QUIT")
							quitColor = (0,0,225)
							quitFlag = True
				else:
					tryQuit = False
					quitColor = (0,0,225)

	if LeftHandOnScreen == True:
		if mainHand == 'Left':
			left_pointer_tip_x = int(leftHandLms[8].x*w)
			left_pointer_tip_y = int(leftHandLms[8].y*h)
			cv2.circle(img, (left_pointer_tip_x,left_pointer_tip_y), 10, (244,244,88), cv2.FILLED)
			if left_pointer_tip_x > 540 and left_pointer_tip_x < 620 and left_pointer_tip_y > 20 and left_pointer_tip_y < 60:
				if tryQuit == False:
					print("Trying To Quit")
					tryQuit = True
					StartT = time.time()
				elif tryQuit == True:
					ct = time.time()
					t = int((ct - StartT) % 60)
					#print(t)
					if t == 1:
						quitColor = (0,225,0)
						#print("COLOR BLUE")
					elif t == 2:
						quitColor = (225,0,0)
						#print("COLOR GREEN")
					elif t == 3:
						#print("QUIT")
						quitColor = (0,0,225)
						quitFlag = True
			else:
				tryQuit = False
				quitColor = (0,0,225)

		

	cv2.putText(img, f'Left Hand: {LeftHandOnScreen}', (10,60), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,0,225), 1)
	cv2.putText(img, f'Right Hand: {RightHandOnScreen}', (10,90), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,0,225), 1)
			

	cTime = time.time()
	fps = 1/(cTime-pTime)
	pTime = cTime

	cv2.putText(img, f'FPS: {int(fps)}', (10,30), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,225), 2)

	cv2.rectangle(img, pt1=(540, 20), pt2=(620, 60), color=quitColor, thickness=4)
	cv2.putText(img, 'Quit', (550,50), cv2.FONT_HERSHEY_PLAIN, 2, quitColor, 1)

	cv2.imshow("Image", img)
	cv2.waitKey(1)
	if quitFlag == True:
		break

cv2.destroyAllWindows()
quit()