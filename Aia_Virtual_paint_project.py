import cv2
import numpy as np

frameWidth = 1080
frameHeight = 720
cap = cv2.VideoCapture(0)
cv2.destroyAllWindows()
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 180)
myColors = [[73, 90, 80, 90, 255, 255], [147, 120, 100, 179, 255, 255], [60, 165, 121, 145, 255, 255],
            [0, 80, 145, 80, 255, 210]]

myColorValues = [[38, 201, 32],
                 [10, 10, 207],
                 [163, 171, 19],
                 [7, 235, 235]]

myPoints = []


def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 5, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        cv2.imshow(str(color[0]), mask)
    return newPoints


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, z = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            # cv2.drawContours (imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 15, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    if img is None:
        break
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)
    cv2.imshow("result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
