import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel')

def getSpeechText():
    r = sr.Recognizer()
    text = ''

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        engine.say('Say the application name')
        engine.runAndWait()
        print('say the name')
        audio = r.listen(source)
        print('done')

    try:
        text = r.recognize_google(audio)

    except:
        pass

    return text

import subprocess as sub

app_name = getSpeechText()

sub.call(
    ["/usr/bin/open", "-W", "-n", "-a", "/Applications/" + app_name + ".app"]
)

engine.say('App Session ended successfully')
engine.runAndWait()
