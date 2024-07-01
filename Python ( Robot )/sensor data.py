mode = ""
import threading, re, os, time, datetime

try:
    import serial

    # Set up Bluetooth serial connection
    bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=9600)
except:
    print("Error with Bluetooth serial connection")

try:
    import RPi.GPIO as GPIO
    import keyboard

    # Set up GPIO pins for the motor controller
    # In this example, we are using pins 7, 11, 13, and 15
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
except:
    print("Error With RPI.GPIO or Keybo")
# Adafruit DHT
try:
    import Adafruit_DHT

    sensor = Adafruit_DHT.DHT11
    pin = 4
except:
    print("Error Adafruit DHT")
# fuzzywuzzy ( Similarity Ratio )
try:
    from fuzzywuzzy import fuzz
except:
    print("Error with fuzzywuzzy ( Similarity Ratio )")
# Text To Speak
try:
    from gtts import gTTS
    from playsound import playsound
except:
    print("Error With gtts and PlaySound")
# Telegram Imports
try:
    import telepot
    from telepot.loop import MessageLoop
except:
    print("Error with Telepot")

# Face Detection
try:
    import cv2
    import cvzone
    from cvzone.FaceMeshModule import FaceMeshDetector

    cap = cv2.VideoCapture(0)
    detector = FaceMeshDetector(maxFaces=1)
except:
    print("Error With Face Detection")

# OLED Display Imports
try:
    import board
    import busio
    import adafruit_ssd1306
    from PIL import Image, ImageDraw, ImageFont

    # Define the OLED display dimensions
    WIDTH = 128
    HEIGHT = 64
    # Initialize the I2C bus and OLED display objects
    i2c = busio.I2C(board.SCL, board.SDA)
    display1 = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
    display2 = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3D)
except:
    print("Error With Oled display's")

# fireBase Cloud Imports
try:
    from firebase_admin import firestore
    from firebase_admin import credentials
    import firebase_admin
    import pyrebase

except:
    print("Error with Firebase_Admin")

# fireBase Cloud Credentials
credPath = {
    "type": "service_account",
    "project_id": "project---ru",
    "private_key_id": "226ae805ac0bfda6b161a83f8c1d94c37bc799d9",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCy7z9lZri81SgE\nPCIWol8iNTZ5YRKRxP+U5N6E40tX1OJMShQJ1d+wdn1KP4sSTtXxZIere2h4rY7Z\naxO0gqmA3gxRBb1OLfv9KKUJCyKm12qYjM/QAD5N9kX5yTWhAnNjOMZHMH1Sp34+\njZqvuozzStKKVuNaTu+X2xFczVt4N0Ab99rGjW9fdnC+UftpRkDXsJagO7CHPPHg\norzVeLGo/wR4tMZTcThW/JR6OIwd/yNs3eb58CYCvraGkRJoflkojKLCKiUe0fKp\n7QCgYA0sr440t3tWTQoO+Nf4WVSMd1I92GcB12OgOl4izf8ABHqhdniXu5Q2t6+3\ngFVytrfJAgMBAAECggEAGovqMOYThFhvbmlpeUgvqwiQA2QGeD/s1y85YCfElsxL\nopve6zKi1DBQGELjJB00GnMaubM+ZaECL3l2W/KCqU7ILwEV+9JQr1dnXLcdNfmB\npA5ICojutWxTJ2LVpQSTD+ZtbERiY2/cB/XEPEwF+1ZfdAy+ADjzzOjAY69H4ca4\n7AQ5GGU8/FQu1YUudii9bmVBHP7gVQ6Em9GEXeG0y0mDCXNXIXG4F9MZmqxqfuXK\nY27aSIsaxbPv93b2yN7PhOqxZdh5lyFZd48+zD5987Ck7lleqmedBF2p/MTJ9FXc\nt0KLGf6OJ3xqrxuc0xgtV/IFs5KD+K/pEE1RgDfebQKBgQDpJCxp0x6IN5zamGki\nkk7wzeweznvCytwWWMjZTyCyJ+XStuqIXfo30dO2rRdEcO1jnzUBtDRYeRA7nAiC\nNY4nRqVmPfd3cxYoy9CljXaOJBmzZePRUkFET6nQHtsM2Gzm8zblbGm7//XsWmX9\nyI8juVDBVoLfM2tbrxLt/Fs9kwKBgQDEen1YcseEdVvpkTN9uzWr2E2NKnQXcXmx\n5SiwA53idpW/9nBP5RDNxOyWWXb6O7bM21g64op0E2r6/2oX+9C4lyYTgekhDmrc\n4TmmoEr9ETSoJoWY6F3UcIou7+6HfvcyhbUBtuAoN6VbtH5Vc6xorQdDGbjI8Fga\noSCbUSTuswKBgQCohIAh4ftAxMn464+a8JxkzMOupNuqOk2JTZWoFdzxSYuCmrq9\n5Qf3DxD0Cvs1elbs2mhLGgF4LdHA9JDl5WYiF5t4YrQcQDC1PlVLRQx7w7ZcCPr6\nE3WfteFt0M/O4iUdbpGwlYN745DTzafJIA3u6YVoqmqggR9Jvyt0oCMnRwKBgFL4\nEtR169EAqiaQvXi7xKdjuSQCqHF55tT7m1nwvQxz3Trp+3WRmq36GZpH/1kePEx3\n1+NN5P+tb4C8uPWVzgcVNOwJ8QOXjgLmTS0TBXeme2ECm2n9vhnGyGOXyFeJgyPf\nmJc3vaLeFMMMDklRhp3Ra36nbwPTkrD0F8ve0UTHAoGALwdQYGgzjAmOHmYPannJ\nbjVnZLUhGGjToTVwL3u2JP93h9/yi9b0O3iXxLmAZqAhC94Ll8TnxoL5CU7PnGuX\nn7X5iw+o6/THXsS1BGvzRLtaM6sg00UbtRc+hyq38l1xra1dX3SpAlt0Run+YCGF\nuuAuGAUX36QN6n0RK+HdUvE=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-fp6ik@project---ru.iam.gserviceaccount.com",
    "client_id": "110657935735128997860",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fp6ik%40project---ru.iam.gserviceaccount.com"
};
try:
    login = credentials.Certificate(credPath)
    firebase_admin.initialize_app(login)
    db = firestore.client()
except:
    print("Error with Firebase LogIn")

# fireBase RealTime DataBase Credentials
config = {
    "apiKey": "AIzaSyAUEYQvNrTXX8uepftMjpSS_dGSXku15Fw",
    "authDomain": "project---ru.firebaseapp.com",
    "databaseURL": "https://project---ru-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "project---ru",
    "storageBucket": "project---ru.appspot.com",
    "messagingSenderId": "777439668308",
    "appId": "1:777439668308:web:2d7e27d226c35e77cba5c1",
    "measurementId": "G-84JSMEP0CC"
};
try:
    firebase = pyrebase.initialize_app(config)
    dbRT = firebase.database()
except:
    print("Error with pyrebase logIn")

# speech to Text
try:
    import speech_recognition as sr

    r = sr.Recognizer()
except:
    print("Error with Speech Recognition")


def updateSensors():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        try:
            db.collection("sensors").document("temp").update({
                "value": "{:.1f}".format(temperature)
            })
            db.collection("sensors").document("humi").update({
                "value": "{:.1f}".format(humidity)
            })
            db.collection("sensors").document("ftemp").update({
                "value": (temperature * 9 / 5) + 32
            })
        except:
            print("Error uploading Humidity and Temperature")
    else:
        print("Failed to retrieve data from DHT11 sensor")
    try:
        temp = os.popen("vcgencmd measure_temp").readline()
        outRaspiTemp = float(temp.replace("temp=", "").replace("'C\n", ""))
        RaspiTemp = "{:.2f}".format(outRaspiTemp)
        db.collection("sensors").document("raspiTemp").update({
            "value": RaspiTemp
        })
    except:
        print("Error with Raspi Temp")
    try:
        db.collection("sensors").document("ic'sTemp").update({"value": "error"})
        db.collection("sensors").document("light").update({"value": "error"})
    except:
        print("Error with ")


def TextToSpeak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("hello.mp3")
    try:
        playsound("hello.mp3")
    except:
        print("file error")


def speechRecognition():
    with sr.Microphone() as source:
        print("Speak something...")
        audio = r.listen(source)
    try:
        # Use Google speech recognition
        text = r.recognize_google(audio)
        return "{}".format(text)
    except sr.UnknownValueError:
        print("Could not understand audio")
        TextToSpeak("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""


def getTimeDate():
    return datetime.datetime.now().strftime("%I:%M:%S %p"), time.strftime("%H:%M"), time.strftime("%d.%b.%y")


def remainder(setTime=0):
    def remainingTime(docId, setTime):
        end = datetime.datetime.now() + datetime.timedelta(minutes=setTime)
        print(end)
        if len(docId) > 1:
            db.collection("remainderList").document(docId).update({
                "endingTime": end
            })
        while True:
            start = datetime.datetime.now()
            duration = end - start
            remainingTime = str(duration)
            if len(docId) > 1:
                try:
                    db.collection("remainderList").document(docId).update({
                        "remainingTime": remainingTime[:-7]
                    })
                except:
                    print("error with update Firebase Status")

            if duration.total_seconds() < 1:
                print("LED OFF")
                if len(docId) > 1:
                    db.collection("remainderList").document(docId).delete()
                else:

                    TextToSpeak(f"remainder")
                break

    if setTime < 1:
        collection = db.collection("remainderList").stream()
        for x in collection:
            if int(x.to_dict()["setTime"]) > 0:
                threading.Thread(target=remainingTime, args=(x.to_dict()["id"], int(x.to_dict()["setTime"]))).start()
    else:
        threading.Thread(target=remainingTime, args=("", setTime)).start()


def SmartLED():
    def remainingTime(docId, setTime):
        end = datetime.datetime.now() + datetime.timedelta(minutes=setTime)
        print(end)
        if len(docId) > 1:
            db.collection("remainderList").document(docId).update({
                "endingTime": end
            })
        while True:
            start = datetime.datetime.now()
            duration = end - start
            remainingTime = str(duration)
            if len(docId) > 1:
                try:
                    db.collection("remainderList").document(docId).update({
                        "remainingTime": remainingTime[:-7]
                    })
                except:
                    print("error with update Firebase Status")

            if duration.total_seconds() < 1:
                print("LED OFF")
                if len(docId) > 1:
                    db.collection("remainderList").document(docId).delete()
                else:

                    TextToSpeak(f"remainder")
                break

    while 1:
        isOn = dbRT.child("isOn").get().val()
        isChange = False
        if isOn == isChange:
            if isOn:
                collection = db.collection("SmartLED").stream()
                for x in collection:
                    if x.to_dict()["isOn"]:
                        if int(x.to_dict()["timer"])>0:
                            remainingTime(x.to_dict()["id"],int(x.to_dict()["timer"]))
                        else:
                            print("LED ON")
                            db.collection("SmartLED").document(x.to_dict()["id"]).update({
                                "active":True
                            })
                    else:
                        db.collection("SmartLED").document(x.to_dict()["id"]).update({
                            "active": False
                        })
                        print("LED OFF")

            else:
                dbRT.child("isOn").set(False)
        else:



def SimilarityRatio(commend, sentence):
    print(fuzz.token_set_ratio(commend, sentence))
    return fuzz.token_set_ratio(commend, sentence)


def Alarm():
    def AlarmCounting(docId, Time, date):
        isTrue = True
        while isTrue:
            T12, T24, Date = getTimeDate()
            if (Date == date):
                try:
                    db.collection("AlarmList").document(docId).update({
                        "update": "Today"
                    })
                except:
                    print("error with update Firebase Status")
                while isTrue:
                    if (time.strftime("%H:%M") == Time):
                        print("Time")
                        isTrue = False
                        # Alarm Sound
                        db.collection("AlarmList").document(docId).delete()
            time.sleep(10)

    collection = db.collection("AlarmList").stream()
    for x in collection:
        if len(x.to_dict()["time"]) > 0 and len(x.to_dict()["date"]) > 0:
            threading.Thread(target=AlarmCounting,
                             args=(x.to_dict()["id"], x.to_dict()["time"], x.to_dict()["date"])).start()


def TelegramBot():
    def action(msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        print('Received: %s' % command)
        print(chat_id)

        if command == '/hi':
            telegram_bot.sendMessage(chat_id,
                                     str("Hi! CircuitDigest\n" + str(time.now.hour) + str(":") + str(time.now.minute)))

        elif command == '/time':

            telegram_bot.sendMessage(chat_id, str(time.now.hour) + str(":") + str(time.now.minute))

        # elif command == '/logo':

        #     telegram_bot.sendPhoto(chat_id, photo="https://i.pinimg.com/avatars/circuitdigest_1464122100_280.jpg")

        # elif command == '/file':

        #     telegram_bot.sendDocument(chat_id, document=open('/home/pi/Aisha.py'))

        # elif command == '/audio':

        #     telegram_bot.sendAudio(chat_id, audio=open('/home/pi/test.mp3'))

    telegram_bot = telepot.Bot('5669993918:AAH34cFJrpZa_Pio76J5gieaXOEY2KB_5V4')
    print(telegram_bot.getMe())
    MessageLoop(telegram_bot, action).run_as_thread()
    print('Up and Running....')
    listOfChat_Id = ["1314922309"]
    telegram_bot.sendMessage("1314922309", "hi")


def sendMsgTelegram(msg):
    telegram_bot = telepot.Bot('5669993918:AAH34cFJrpZa_Pio76J5gieaXOEY2KB_5V4')
    telegram_bot.sendMessage("1314922309", msg)


def detectFace():
    while True:
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img, draw=False)
        if faces:
            face = faces[0]
            pointLeft = face[145]
            pointRight = face[374]
            # Drawing
            # cv2.line(img, pointLeft, pointRight, (0, 200, 0), 3)
            # cv2.circle(img, pointLeft, 5, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, pointRight, 5, (255, 0, 255), cv2.FILLED)
            w, _ = detector.findDistance(pointLeft, pointRight)
            W = 6.3
            # # Finding the Focal Length
            # d = 50
            # f = (w*d)/W
            # print(f)
            # Finding distance
            f = 840
            d = (W * f) / w
            print(int(d))
            cvzone.putTextRect(img, f'Depth: {int(d)}cm',
                               (face[10][0] - 100, face[10][1] - 50),
                               scale=2)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def manualModeWithKeyboard():
    # Define a function to move the car forward
    def move_forward():
        GPIO.output(7, GPIO.HIGH)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.LOW)

    # Define a function to move the car backward
    def move_backward():
        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.HIGH)

    # Define a function to turn the car left
    def turn_left():
        GPIO.output(7, GPIO.HIGH)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.HIGH)

    # Define a function to turn the car right
    def turn_right():
        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.LOW)

    # Define a function to stop the car
    def stop_car():
        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)

    # Loop to listen for keyboard inputs
    if mode == "keyBoard":
        while True:
            if keyboard.is_pressed('w'):
                move_forward()
            elif keyboard.is_pressed('s'):
                move_backward()
            elif keyboard.is_pressed('a'):
                turn_left()
            elif keyboard.is_pressed('d'):
                turn_right()
            else:
                stop_car()
            # Delay to allow the car to respond to keyboard inputs
            time.sleep(0.1)
            if mode != "app":
                break
    elif mode == "app":
        while True:
            MoveCar = db.child("MoveCar").get().val()
            if MoveCar == 'w':
                # move_forward()
                print("move")
                db.child("MoveCar").set("")
            elif MoveCar == 's':
                print("move")
                # move_backward()
                db.child("MoveCar").set("")
            elif MoveCar == 'a':
                print("move")
                # turn_left()
                db.child("MoveCar").set("")
            elif MoveCar == 'd':
                print("move")
                # turn_right()
                db.child("MoveCar").set("")
            else:
                time.sleep(1)
                print("stop")
                # stop_car()
            # Delay to allow the car to respond to keyboard inputs
            time.sleep(0.1)
            if mode != "app":
                break
    elif mode == "btCar":
        while True:
            data = bluetoothSerial.readline().decode().strip()

            if data == "F":
                move_forward()
            elif data == "B":
                move_backward()
            elif data == "L":
                turn_left()
            elif data == "R":
                turn_right()
            elif data == "S":
                stop_car()
            else:
                print("Invalid command")


def updateDisplayText():
    display1.fill(0)
    display1.show()
    display2.fill(0)
    display2.show()
    font1 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 10)
    text1 = "Hello World!"
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 8)
    text2 = "This is OLED display 2"
    image1 = Image.new("1", (WIDTH, HEIGHT))
    draw1 = ImageDraw.Draw(image1)
    image2 = Image.new("1", (WIDTH, HEIGHT))
    draw2 = ImageDraw.Draw(image2)
    draw1.text((0, 10), text1, font=font1, fill=255)
    draw2.text((0, 10), text2, font=font2, fill=255)
    display1.image(image1)
    display1.show()
    display2.image(image2)
    display2.show()


def updateDisplayImage():
    display1.fill(0)
    display1.show()
    display2.fill(0)
    display2.show()
    image = Image.open("image.png").convert("1")
    image1 = Image.new("1", (WIDTH, HEIGHT))
    draw1 = ImageDraw.Draw(image1)
    image2 = Image.new("1", (WIDTH, HEIGHT))
    draw2 = ImageDraw.Draw(image2)
    image1.paste(image, (0, 0))
    image2.paste(image, (0, 0))
    display1.image(image1)
    display1.show()
    display2.image(image2)
    display2.show()

0
def getModeFromPyrebase():
    global mode
    while True:
        time.sleep(5)
        mode = db.child("mode").get().val()


# # SimilarityRatio("hello ru detect my face and track me","detect face and move")
threading.Thread(target=SmartLED).start()
#
# while True:
#     print(mode)
#     manualModeWithKeyboard()
#     time.sleep(1)
#     # commend = speechRecognition()
#     # print(commend)
#     # #commend = "set remainder for 1 minutes"
#     # if SimilarityRatio(commend,"set remainder for")>70:
#     #     numbers = re.findall(r'\d+(?:\.\d+)?', commend)
#     #     print(int(numbers[0]))
#     #     remainder(int(numbers[0]))
#
