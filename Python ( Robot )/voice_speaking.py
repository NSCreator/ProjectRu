import speech_recognition as sr
import datetime
import wikipedia
import pyttsx3
#from google_trans_new import google_translator
#import subprocess
#import pywhatkit
#import webbrowser
#from GoogleNews import GoogleNews
#from google_trans_new import google_translator
#import yagmail

global wikisearch
engine = pyttsx3.init()
recognizer = sr.Recognizer()
#googlenews = GoogleNews()
# voices = engine.getProperty('voices')
# engine.setProperty('voice',voices[1].id)


class speaker_mic:
    def __init__(self):
        self.speaker()
        self.mic()
        self.trans()
        self.cmd()
    def speaker(self):
        engine.say(wikisearch)
    def mic(self):
        with sr.Microphone() as source:
            print('Clearing background noise...Please wait')
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("waiting for your message...")
            recordedaudio = recognizer.listen(source)
            print('Done recording')
            #   print('Printing your message...Please wait')
            #   text = recognizer.recognize_google(recordedaudio, language='en-US')
            #   print('Your Message:{}', format(text))
            try:
                text = recognizer.recognize_google(recordedaudio, language='en_US')
                #result = recognizer.recognize_google(audio, language='ta-IN')
                text = text.lower()
                print('Your message:', format(text))

            except Exception as ex:
                print(ex)

    def wikipedia(self):
        wikisearch = wikipedia.summary(text)

    def cmd(self):

        if 'chrome' in text:
            a = 'Opening chrome..'
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
            a = 'opening youtube..'
            engine.say(a)
            engine.runAndWait()
            pywhatkit.playonyt(text)
        if 'youtube' in text:
            b = 'opening youtube'
            engine.say(b)
            engine.runAndWait()
            webbrowser.open('www.youtube.com')
    def google(self):
        if 'headlines' in text:
            engine.say('Getting news for you ')
            engine.runAndWait()
            googlenews.get_news('Today news')
            googlenews.result()
            a = googlenews.gettext()
            print(*a[1:5], sep=',')

        if 'tech' in text:
            engine.say('Getting news for you ')
            engine.runAndWait()
            googlenews.get_news('Tech')
            googlenews.result()
            a = googlenews.gettext()
            print(*a[1:5], sep=',')

        if 'politics' in text:
            engine.say('Getting news for you ')
            engine.runAndWait()
            googlenews.get_news('Politics')
            googlenews.result()
            a = googlenews.gettext()
            print(*a[1:5], sep=',')

        if 'sports' in text:
            engine.say('Getting news for you ')
            engine.runAndWait()
            googlenews.get_news('Sports')
            googlenews.result()
            a = googlenews.gettext()
            print(*a[1:5], sep=',')

        if 'cricket' in text:
            engine.say('Getting news for you ')
            engine.runAndWait()
            googlenews.get_news('cricket')
            googlenews.result()
            a = googlenews.gettext()
            print(*a[1:5], sep=',')






engine.runAndWait()



"""
    def trans(self):
        langinput = input('Type the language you want to convert:')
        translator = google_translator()
        translate_text = translator.translate(str(result), lang_tgt=str(langinput))
        print(translate_text)
        engine.say(str(translate_text))
        engine.runAndWait()



trans()"""
"""
#Automate mails:
reciever=' Receiver's email id'
message=text
sender=yagmail.SMTP('Sender's email id ')
sender.send(to=reciever,subject='This is an automated mail',contents=message)"""
"""