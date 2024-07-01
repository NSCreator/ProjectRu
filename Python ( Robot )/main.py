import math

import pyttsx3
import speech_recognition as sr
recognizer = sr.Recognizer()
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)


from cvzone.HandTrackingModule import HandDetector
# cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector1 = HandDetector(detectionCon=0.8,maxHands=1)
# x is raw distances and y is value in cm
x = [300,245,200,170,145,130,112,103,93,87,80,75,70,67,62,59,57]
y = [20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
coff = numpy.polyfit(x, y, 2)

def voice(in_data, gender):
    engine = pyttsx3.init()
    engine.setProperty('rate', 190)
    voices = engine.getProperty('voices')
    engine.setProperty('volume', 1.0)
    if gender == "M":
        engine.setProperty('pitch', 75)
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('pitch', 75)
        engine.setProperty('voice', voices[1].id)
    engine.say(in_data)
    engine.runAndWait()


def move_head(servo1_angle, servo2_angle):
    pass


def speech_to_text():
    text =""
    with sr.Microphone() as source:
        print('Clearing background noise...Please wait')
        recognizer.adjust_for_ambient_noise(source, duration=1.5)
        print("waiting for your message...")
        recordedaudio = recognizer.listen(source)
        print('Done recording')
        try:
            text = recognizer.recognize_google(recordedaudio, language='en_US')
            text = text.lower()
            print('Your message:', format(text))

        except Exception as ex:
            print(ex)
        return text


    # def wikipedia(self):
    #     wikisearch = wikipedia.summary(text)
    #
    # def cmd(self):
    #
    #     if 'chrome' in text:
    #         a = 'Opening chrome..'
    #         engine.say(a)
    #         engine.runAndWait()
    #         programName = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    #         subprocess.Popen([programName])
    #     if 'time' in text:
    #         time = datetime.datetime.now().strftime('%I:%M %p')
    #         print(time)
    #         engine.say(time)
    #         engine.runAndWait()
    #     if 'play' in text:
    #         a = 'opening youtube..'
    #         engine.say(a)
    #         engine.runAndWait()
    #         pywhatkit.playonyt(text)
    #     if 'youtube' in text:
    #         b = 'opening youtube'
    #         engine.say(b)
    #         engine.runAndWait()
    #         webbrowser.open('www.youtube.com')
    # def google(self):
    #     if 'headlines' in text:
    #         engine.say('Getting news for you ')
    #         engine.runAndWait()
    #         googlenews.get_news('Today news')
    #         googlenews.result()
    #         a = googlenews.gettext()
    #         print(*a[1:5], sep=',')
    #
    #     if 'tech' in text:
    #         engine.say('Getting news for you ')
    #         engine.runAndWait()
    #         googlenews.get_news('Tech')
    #         googlenews.result()
    #         a = googlenews.gettext()
    #         print(*a[1:5], sep=',')
    #
    #     if 'politics' in text:
    #         engine.say('Getting news for you ')
    #         engine.runAndWait()
    #         googlenews.get_news('Politics')
    #         googlenews.result()
    #         a = googlenews.gettext()
    #         print(*a[1:5], sep=',')
    #
    #     if 'sports' in text:
    #         engine.say('Getting news for you ')
    #         engine.runAndWait()
    #         googlenews.get_news('Sports')
    #         googlenews.result()
    #         a = googlenews.gettext()
    #         print(*a[1:5], sep=',')
    #
    #     if 'cricket' in text:
    #         engine.say('Getting news for you ')
    #         engine.runAndWait()
    #         googlenews.get_news('cricket')
    #         googlenews.result()
    #         a = googlenews.gettext()
    #         print(*a[1:5], sep=',')


def distance_detection_with_camera():
    while True:
        sucess, img = cap.read()
        img, faces = detector.findFaceMesh(img, draw=False)

        if faces:
            face = faces[0]
            pointLeft = face[145]
            pointRight = face[374]
            # cv2.line(img, pointLeft, pointRight, (0, 200, 0), 3)
            # cv2.circle(img, pointLeft, 5, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, pointRight, 5, (255, 0, 255), cv2.FILLED)
            w, _ = detector.findDistance(pointLeft, pointRight)
            W = 6.5
            # Finding Focal Length
            # d = 50
            # f =(w*d)/W
            # Finding Distance
            f = 840
            d = (W * f) / w
            # printing distance number on the face
            cvzone.putTextRect(img, f"Dist {int(d)}cm",
                               (face[10][0] - 100, face[10][1] - 50),
                               scale=2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


def hand_detection_with_camera():
    while True:
        success, img = cap.read()
        hands = detector1.findHands(img, draw=False)
        if hands:
            lmList = hands[0]['lmList']
            x, y, w, h = hands[0]['bbox']
            x1, y1, z1 = lmList[5]
            x2, y2, z2 = lmList[17]
            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
            A, B, C = coff
            distanceCM = A * distance ** 2 + B * distance + C
            print(distanceCM)

            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
            cvzone.putTextRect(img, f"{int(distanceCM)} cm", (x + 5, y - 10))
        cv2.imshow("Image", img)
        cv2.waitKey(1)


#voice(speech_to_text(), "")
out = speech_to_text()
voice(out, "")
if ("distances"or "distance" )and "you" and "me"and"face"in out :
    distance_detection_with_camera()
if ("distances"or "distance" )and "hand"in out :
    hand_detection_with_camera()