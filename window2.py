from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import json
import pyttsx3
import requests
import urllib.request
import os
import wikipedia
import wolframalpha
import pymongo
import speech_recognition as sr

data={}

with open('currentUser.txt') as json_file:
    data = json.load(json_file)

userName = data['info'][0]

engine = pyttsx3.init()

engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel')


def weather():

    encodedAddress = simpledialog.askstring("Location Required","Enter the location")

    key = '<<Key>>'

    api_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + encodedAddress + '&key=' + key

    response_1 = requests.get(api_url)

    data = response_1.json()

    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']

    key_2 = '<<Key>>'

    ds_url = 'https://api.darksky.net/forecast/' + str(key_2) + '/' + str(lat) + ',' + str(lng)

    uh = urllib.request.urlopen(ds_url)
    data_2 = uh.read()

    data_2 = json.loads(data_2.decode("utf-8"))


    def f2c(fah):
        fahrenheit = float(fah)
        celsius = (fahrenheit - 32) / 1.8
        return celsius

    if encodedAddress != "":
        messagebox.showinfo("Temperature Report",'Temperature for ' + encodedAddress + '\nTemp : ' + str(f2c(data_2['currently']['temperature']))[0:4] + ' C\nStatus : '+data_2['daily']['icon']+'\nSummary : '+data_2['daily']['summary'])


def news():

    os.system('python news.py')

def application():

    os.system('python app_open.py')

def topic():

    window.iconify()

    title = simpledialog.askstring("Topic Required","Please enter the topic name")
    summary = wikipedia.summary(title, sentences=2)
    engine.say('This is what i found on ' + title)
    engine.runAndWait()

    messagebox.showinfo('Results on '+title,summary)

    os.system('python -W ignore window2.py')

def wolfram():

    window.iconify()

    app_id = "<<App_ID>>"
    client = wolframalpha.Client(app_id)

    ques = simpledialog.askstring("Query Required", "Please enter some query")

    res = client.query(ques)
    answer = next(res.results).text

    engine.say('This is what i got')
    engine.runAndWait()

    messagebox.showinfo(ques,answer)

    os.system('python -W ignore window2.py')

def google():

    api_key = '<<API_Key>>'
    ques = simpledialog.askstring("Query Required", "Please enter some query")
    api_url='https://www.googleapis.com/customsearch/v1?key='+api_key+'&cx=004813015154938053204:qhbukfjnmfq&q='+ques

    response = requests.get(api_url)

    data = response.json()

    txt=''
    for i in data['items']:
        txt = txt+i['title']+'\n'+i['snippet']+'\n\n'

    messagebox.showinfo(ques, txt)

def saveNote():

    window.iconify()

    os.system('python -W ignore saveNote.py')

    engine.say('Note Saved')
    engine.runAndWait()

    os.system('python -W ignore window2.py')

def quickNotes():

    window.iconify()

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[userName]
    mycol = mydb["notes"]

    notes = mycol.find({})

    c = 1
    notes_list = ''
    temp_note_listings = list()
    for i in notes:
        txt = '[' + str(c) + '] - ' + i['title'] + '\n' + i['note'] + '\n'
        temp_note_listings.append(i['title'])
        c += 1
        notes_list = notes_list + txt

    try:
        engine.say('Here are all the notes')
        engine.runAndWait()
    except:
        pass

    messagebox.showinfo('These are the notes for '+userName, notes_list)

    os.system('python -W ignore window2.py')

window = Tk()

window.title("Tyr Assistant App")

window.geometry('200x300+450+275')

lbl = Label(window,text='These are your options :')
lbl.grid(column=1,row=1)

lbl2 = Label(window,text='  ')
lbl2.grid(column=1,row=0)

lbl1 = Label(window,text='')
lbl1.grid(column=1,row=2)

lbl3 = Label(window,text=" ")
lbl3.grid(column=0,row=2)

rad1 = Radiobutton(window, text='Weather', value=1,command=weather)

rad2 = Radiobutton(window, text='News', value=2, command=news)

rad3 = Radiobutton(window, text='Open Application', value=3, command=application)

rad4 = Radiobutton(window, text='Search a topic', value=4, command=topic)

rad5 = Radiobutton(window, text='Do a query', value=5, command=wolfram)

rad6 = Radiobutton(window, text='Save a quick note', value=6, command=saveNote)

rad7 = Radiobutton(window, text='Quick Notes', value=7, command=quickNotes)

rad8 = Radiobutton(window, text='', value=8)

rad8.select()

rad1.grid(column=1, row=3, sticky=W)

rad2.grid(column=1, row=4, sticky=W)

rad3.grid(column=1, row=5, sticky=W)

rad4.grid(column=1, row=6, sticky=W)

rad5.grid(column=1, row=7, sticky=W)

rad6.grid(column=1, row=8, sticky=W)

rad7.grid(column=1, row=9, sticky=W)

def voice():
    def getSpeechText():
        r = sr.Recognizer()
        text = ''

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)

            engine.say('Say the choice')
            engine.runAndWait()
            print('say the choice')
            audio = r.listen(source)
            print('done')

        try:
            text = r.recognize_google(audio)

        except:
            pass

        return text

    choice = getSpeechText()

    if choice.strip().lower()=='weather':
        weather()
    elif choice.strip().lower()=='news':
        news()
    elif choice.strip().lower()=='open application':
        application()
    elif choice.strip().lower()=='search a topic':
        topic()
    elif choice.strip().lower()=='do a query':
        wolframalpha()
    elif choice.strip().lower()=='save a quick note':
        saveNote()
    elif choice.strip().lower()=='quick notes':
        quickNotes()

lbl4 = Label(window,text='  ')
lbl4.grid(column=1,row=10)

btn = Button(window,text="Voice Input", command=voice)

btn.grid(column=1, row=11)

window.mainloop()