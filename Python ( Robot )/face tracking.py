import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import time

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=2)
servoAngle = 90
while True:
    sucess, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=True)

    if faces:
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374]
        cv2.line(img, pointLeft, pointRight, (0, 200, 0), 3)
        cv2.circle(img, pointLeft, 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, pointRight, 5, (255, 0, 255), cv2.FILLED)
        w, _ = detector.findDistance(pointLeft, pointRight)
        W = 6.5
        f = 840
        d = (W*f)/w
        point_x = (pointLeft[0] + pointRight[0])//2
        point_y = (pointLeft[1] + pointRight[1]) // 2
        if point_x>280 and point_x<380 :
            print("stop")
        elif point_x<=280:
            print("left")
        else:
            print("right")
        if point_y > 230 and point_y < 330:
            print("stop")
        elif point_y <= 230:
            servoAngle = servoAngle+1
        else:
            servoAngle = servoAngle-1
        if servoAngle >20 and servoAngle < 160:
            pass
        else:
            if point_y > 230 and point_y < 330:
                print("stop")
            elif point_y <= 230:
                print("backwards")
            else:
                print("forwards")
        print(servoAngle)
        cvzone.putTextRect(img, f"Dist {int(d)}cm",
                           (face[10][0]-100, face[10][1]-50),
                           scale=2)
        # time.sleep(0.08)
    cv2.imshow("Image", img)
    cv2.waitKey(1)