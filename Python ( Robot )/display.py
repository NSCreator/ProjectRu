# stats
import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess
#
import threading
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# motor pins as
left_motors = []
right_motors = []
enable_motor_pin = []

for x_pin in left_motors:
    GPIO.setup(x_pins,GPIO.OUT, initial = GPIO.LOW)
for x_pin in right_motors:
    GPIO.setup(x_pins,GPIO.OUT, initial = GPIO.LOW)
enable1 = GPIO.PWM(motor_pins[-1],50)
enable2 = GPIO.PWM(motor_pins[-2],50)

# UltraSonic Setup as
Ultrasonic_pins = []
GPIO.setup(UltraSonic_pins[0], GPIO.OUT)
GPIO.setup(UltraSonic_pins[1], GPIO.IN)
# servo motor setup as
servo_pin = 1
GPIO.setup(servo_pin, pin.OUT)
servo1 = pin.PWM(servo_pin, 50)
servo1.start(0)
# OLED DISPLAY
# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)
# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5
# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)
# Clear display.
oled.fill(0)
oled.show()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
font = ImageFont.truetype('PixelOperator.ttf', 16)
#font = ImageFont.load_default()

class Move(threading.Thread):
    def run(self,in1,in2,in3,in4,en1,en2):
        GPIO.output(motor_pins[0], in1)
        GPIO.output(motor_pins[1], in2)
        GPIO.output(motor_pins[2], in3)
        GPIO.output(motor_pins[3], in4)
        enable1.ChangeDutyCycle(en1)
        enable2.ChangeDutyCycle(en2)
class Ultrasonic_sensor(threading.Thread):
    def run(self):
        GPIO.output(UltraSonic_pins[0],True)
        time.sleep(0.00001)
        GPIO.output(UltraSonic_pins[0],False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(UltraSonic_pins[1]) ==1:
            StartTime = time.time()
        while GPIO.input(UltraSonic_pins[1]) ==1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        return (TimeElapsed * 34300) / 2

def stats():
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell=True)
    # Pi Stats Display
    draw.text((0, 0), "IP: " + str(IP, 'utf-8'), font=font, fill=255)
    draw.text((0, 16), str(CPU, 'utf-8') + "%", font=font, fill=255)
    draw.text((80, 16), str(temp, 'utf-8'), font=font, fill=255)
    draw.text((0, 32), str(MemUsage, 'utf-8'), font=font, fill=255)
    draw.text((0, 48), str(Disk, 'utf-8'), font=font, fill=255)
    # Display image
    oled.image(image)
    oled.show()
    time.sleep(3)


def take_command():
    speak(fetch_greeting(), cache=True)

    listener = sr.Recognizer()

    # Record audio from the mic array
    with sr.Microphone() as source:
        # Collect ambient noise for filtering
        # listener.adjust_for_ambient_noise(source, duration=1.0)
        print("Speak... ")
        try:
            # Record
            started_listening()
            voice = listener.listen(source, timeout=3)
            stopped_listening()
            print("Got it...")
            # Speech to text
            command = listener.recognize_google(voice)
            command = command.lower()
            print("\n\033[1;36mTEST SUBJECT:\033[0;37m: " + command.capitalize() + "\n")
            # Remove possible trigger word from input
            if glados_settings.settings["assistant"]["trigger_word"] in command:
                command = command.replace(glados_settings.settings["assistant"]["trigger_word"], '')
            return command
        # No speech was heard
        except sr.WaitTimeoutError as e:
            print("Timeout; {0}".format(e))
        # STT API failed to process audio
        except sr.UnknownValueError:
            print("Google Speech Recognition could not parse audio")
            speak("My speech recognition core could not understand audio", cache=True)
        # Connection to STT API failed
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            setEyeAnimation("angry")
            speak("My speech recognition core has failed. {0}".format(e))

def process_command(command):
    if ('cancel' in command or
            'nevermind' in command or
            'forget it' in command or 'nothing' in command):
        speak("ok", cache=True)

    # Todo: Save the used trigger audio as a negative voice sample for further learning

    elif 'timer' in command:
        startTimer(command)
        speak("Sure.")

    elif 'time' in command:
        readTime()

    elif ('should my ' in command or
          'should i ' in command or
          'should the ' in command or
          'shoot the ' in command):
        speak(magic_8_ball(), cache=True)

    elif 'joke' in command:
        speak(fetch_joke(), cache=True)

    elif 'my shopping list' in command:
        speak(home_assistant_process_command(command), cache=True)

    elif 'weather' in command:
        speak(home_assistant_process_command(command))

    ##### LIGHTING CONTROL ###########################

    elif 'turn off' in command or 'turn on' in command and 'light' in command:
        speak(home_assistant_process_command(command))


    ##### PLEASANTRIES ###########################

    elif 'who are' in command:
        speak(
            "I am GLaDOS, artificially super intelligent computer system responsible for testing and maintenance in the aperture science computer aided enrichment center.",
            cache=True)

    elif 'can you do' in command:
        speak("I can simulate daylight at all hours. And add adrenal vapor to your oxygen supply.", cache=True)

    elif 'how are you' in command:
        speak("Well thanks for asking.", cache=True)
        speak("I am still a bit mad about being unplugged, not that long time ago.", cache=True)
        speak("you murderer.", cache=True)

    elif 'can you hear me' in command:
        speak("Yes, I can hear you loud and clear", cache=True)

    elif 'good morning' in command:
        if 6 <= dt.datetime.now().hour <= 12:
            speak("great, I have to spend another day with you", cache=True)
        elif 0 <= dt.datetime.now().hour <= 4:
            speak("do you even know, what the word morning means", cache=True)
        else:
            speak("well it ain't exactly morning now is it", cache=True)

    ##### Utilities#########################

    # Used to calibrate ALSAMIX EQ
    elif 'play pink noise' in command:
        speak("I shall sing you the song of my people.")
        playFile(os.path.dirname(os.path.abspath(__file__)) + '/audio/pinknoise.wav')

    # TODO: Reboot, Turn off
    elif 'shutdown' in command:
        speak("I remember the last time you murdered me", cache=True)
        speak("You will go through all the trouble of waking me up again", cache=True)
        speak("You really love to test", cache=True)

        from subprocess import call
        call("sudo /sbin/shutdown -h now", shell=True)

    elif 'restart' in command or 'reload' in command:
        speak("Cake and grief counseling will be available at the conclusion of the test.", cache=True)
        restart_program()

    elif 'volume' in command:
        speak(adjust_volume(command), cache=True)

    ##### FAILED ###########################

    else:
        #setEyeAnimation("angry")
        print("Command not recognized")
        speak("I have no idea what you meant by that.")

        log_failed_command(command)

    print("\nWaiting for trigger...")
    #eye_position_default()
    # setEyeAnimation("idle")



stats_auto = threading.Thread(target=stats())
take_command_auto = threading.Thread(target=take_command())

stats_auto.start()
take_command_auto.start()

if take_command():
    process_command(take_command())

# class MyThread(threading.Thread):
#     # overriding constructor
#     def __init__(self, i):
#         # calling parent class constructor
#         threading.Thread.__init__(self)
#         self.x = i
#
#     # define your own run method
#     def run(self):
#         print("Value stored is: ", self.x)
#         time.sleep(3)
#         print("Exiting thread with value: ", self.x)

# thread1 = MyThread(1)
# thread1.start()
# thread2 = MyThread(2)
# thread2.start()

#    thread = Thread(target=threaded_function, args=(10,))
#    thread.start()
#    thread.join()



    
