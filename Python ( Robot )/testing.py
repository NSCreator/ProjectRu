import speech_recognition as sr
import datetime
import wikipedia
import pyttsx3
#import subprocess
#import pywhatkit
#import webbrowser
#from GoogleNews import GoogleNews
#from google_trans_new import google_translator
#import yagmail

#engine = pyttsx3.init()
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print('Clearing background noise...Please wait')
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("waiting for your message...")
    audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio)
    print('Done recording')
'''
try:
    print('Printing your message...Please wait')
    text = recognizer.recognize_google(recordedaudio, language='en-US')
    print('Your Message:{}', format(text))

except Exception as ex:
    print(ex)

#Input data
wikisearch = wikipedia.summary(text)
engine.say(wikisearch)
engine.runAndWait()'''
"""



engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
recognizer=sr.Recognizer()

def cmd():
    with sr.Microphone() as source:
        print("Clearing background noises...Pleasw wait")
        recognizer.adjust_for_ambient_noise(source,duration=0.5)
        print('Ask me anything..')
        recordedaudio=recognizer.listen(source)
    try:
        text=recognizer.recognize_google(recordedaudio,language='en_US')
        text=text.lower()
        print('Your message:',format(text))

    except Exception as ex:
        print(ex)
    if 'chrome'in text:
        a='Opening chrome..'
        engine.say(a)
        engine.runAndWait()
        programName = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([programName])
    if 'time' in text:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        engine.say(time)
        engine.runAndWait()
    if 'play' in text:
        a='opening youtube..'
        engine.say(a)
        engine.runAndWait()
        pywhatkit.playonyt(text)
    if 'youtube' in text:
        b='opening youtube'
        engine.say(b)
        engine.runAndWait()
        webbrowser.open('www.youtube.com')
while True:
    cmd()"""
"""
import speech_recognition as sr
import yagmail

recognizer=sr.Recognizer()
with sr.Microphone() as source:
    print('Clearing background noise..')
    recognizer.adjust_for_ambient_noise(source,duration=1)
    print("waiting for your message...")
    recordedaudio=recognizer.listen(source)
    print('Done recording..!')
try:
    print('Printing the message..')
    text=recognizer.recognize_google(recordedaudio,language='en-US')

    print('Your message:{}'.format(text))

except Exception as ex:
    print(ex)

#Automate mails:

reciever=' Receiver's email id'
message=text
sender=yagmail.SMTP('Sender's email id ')
sender.send(to=reciever,subject='This is an automated mail',contents=message)"""


"""
import speech_recognition as sr 
import pyttsx3

#Intialization
googlenews = GoogleNews()
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
recognizer=sr.Recognizer()

#Commands
def cmd():
    with sr.Microphone() as source:
        print("Clearing background noises...Please wait")
        recognizer.adjust_for_ambient_noise(source,duration=0.5)
        print('Ask me anything..')
        recordedaudio=recognizer.listen(source,timeout=1)
        print("Done recording..!")
    try:
        text=recognizer.recognize_google(recordedaudio,language='en_US')
        text=text.lower()
        print('Your message:',format(text))

    except Exception as ex:
        print(ex)

    if 'headlines' in text:
        engine.say('Getting news for you ')
        engine.runAndWait()
        googlenews.get_news('Today news')
        googlenews.result()
        a=googlenews.gettext()
        print(*a[1:5],sep=',')

    if 'tech' in text:
        engine.say('Getting news for you ')
        engine.runAndWait()
        googlenews.get_news('Tech')
        googlenews.result()
        a=googlenews.gettext()
        print(*a[1:5],sep=',')

    if 'politics' in text:
        engine.say('Getting news for you ')
        engine.runAndWait()
        googlenews.get_news('Politics')
        googlenews.result()
        a=googlenews.gettext()
        print(*a[1:5],sep=',')

    if 'sports' in text:
        engine.say('Getting news for you ')
        engine.runAndWait()
        googlenews.get_news('Sports')
        googlenews.result()
        a=googlenews.gettext()
        print(*a[1:5],sep=',')

    if 'cricket' in text:
        engine.say('Getting news for you ')
        engine.runAndWait()
        googlenews.get_news('cricket')
        googlenews.result()
        a=googlenews.gettext()
        print(*a[1:5],sep=',')
cmd()"""


"""
import speech_recognition as sr
from google_trans_new import google_translator
import pyttsx3 
recognizer=sr.Recognizer()
engine = pyttsx3.init()
with sr.Microphone() as source: 
    print('Clearing background noise...')
    recognizer.adjust_for_ambient_noise(source,duration=1)
    print('Waiting for message..') 
    audio = recognizer.listen(source,timeout=1)
    print('Done recording..') 
try:
    print('Recognizing..')
    result = recognizer.recognize_google(audio,language='ta-IN')
except Exception as ex:
    print(ex)
def trans():
    langinput=input('Type the language you want to convert:')
    translator = google_translator()  
    translate_text = translator.translate(str(result),lang_tgt=str(langinput))  
    print(translate_text)
    engine.say(str(translate_text))
    engine.runAndWait()
trans()"""